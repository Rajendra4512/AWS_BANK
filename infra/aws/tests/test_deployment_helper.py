import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[3]
TEMPLATE = ROOT / "infra" / "aws" / "user_data.sh.tftpl"
IAM = ROOT / "infra" / "aws" / "iam.tf"


class BootstrapTemplateTests(unittest.TestCase):
    def test_auto_shutdown_policy_is_self_instance_scoped(self):
        text = IAM.read_text()
        self.assertIn('sid       = "StopOwnAwsBankInstance"', text)
        self.assertIn('actions   = ["ec2:StopInstances"]', text)
        self.assertIn('variable = "aws:userid"', text)
        self.assertIn('values   = ["*:$${ec2:InstanceID}"]', text)
        self.assertIn('variable = "ec2:SourceInstanceARN"', text)
        self.assertNotIn('sid       = "StopTaggedAwsBankInstance"', text)
        self.assertNotIn('ec2:ResourceTag/Name', text)
        self.assertNotIn('actions   = ["ec2:*"]', text)

    def test_bootstrap_hardening_contract(self):
        text = TEMPLATE.read_text()
        bootstrap = text.split("cat > /usr/local/sbin/aws-bank-container-run", 1)[0]
        self.assertIn("VOLUME_WAIT_ATTEMPTS=60", text)
        self.assertIn("expected EBS volume $DATA_VOLUME_ID did not appear as exactly one device", text)
        self.assertIn("command -v mkfs.xfs", text)
        self.assertIn("dnf install -y xfsprogs", text)
        self.assertIn('chown root:root "$ENV_FILE"', text)
        self.assertIn('chmod 600 "$ENV_FILE"', text)
        self.assertIn("install -d -m 0755 /run/lock\nexec 9>/run/lock/aws-bank-deploy.lock\nflock", bootstrap)
        self.assertEqual(text.count("install -d -m 0755 /run/lock"), 4)
        self.assertEqual(text.count("exec 9>/run/lock/aws-bank-deploy.lock"), 3)
        self.assertIn('[[ "$FS_TYPE" == "xfs" ]] || die "existing filesystem is not xfs; refusing reformat"', text)
        self.assertIn('[[ $${#BLOCK_TYPES[@]} -eq 1 && "$${BLOCK_TYPES[0]}" == "disk" ]]', text)
        self.assertIn('[[ "$(readlink -f "$MOUNT_SOURCE")" == "$DEVICE" ]] || die "mounted source mismatch"', text)
        self.assertIn("MAX_RUNTIME_SECONDS=14400", text)
        self.assertIn("http://169.254.169.254/latest/api/token", text)
        self.assertIn("aws ec2 stop-instances --instance-ids", text)
        self.assertIn("aws-bank-extend-session HOURS (1-12)", text)
        self.assertIn("systemctl start --no-block aws-bank-auto-shutdown.service", text)


class DeploymentHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.name != "posix" or shutil.which("bash") is None or shutil.which("flock") is None:
            raise unittest.SkipTest("bash/flock Linux test environment is required")
        cls.temp = tempfile.TemporaryDirectory(prefix="aws-bank-helper-")
        cls.root = Path(cls.temp.name)
        cls.data = cls.root / "data"
        cls.bin = cls.root / "bin"
        cls.state = cls.root / "state"
        cls.data.mkdir()
        cls.bin.mkdir()
        cls.state.mkdir()
        cls._install_scripts(cls._render_template())
        cls._write_mocks()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @classmethod
    def _render_template(cls):
        text = TEMPLATE.read_text()
        values = {
            "aws_region": "ap-southeast-2",
            "image_uri": "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/aws-bank@sha256:" + "0" * 64,
            "data_volume_id": "vol0123456789abcdef0",
            "bootstrap_password_parameter": "/banklab/development/bootstrap-password",
            "session_secret_parameter": "/banklab/development/session-secret",
            "bucket_name": "aws-bank-development-artifacts-example",
            "artifact_prefix": "models/development",
            "log_group_name": "/aws/aws-bank/development",
        }
        for key, value in values.items():
            text = text.replace("${" + key + "}", value)
        return text.replace("$${", "${")

    @classmethod
    def _extract(cls, text, command, marker):
        start = f"cat > /usr/local/sbin/{command} <<'{marker}'\n"
        return text.split(start, 1)[1].split(f"\n{marker}", 1)[0]

    @classmethod
    def _sandbox(cls, script):
        return (
            script.replace("/usr/local/sbin", str(cls.bin))
            .replace("/srv/aws-bank-data", str(cls.data))
            .replace("/run/lock/aws-bank-deploy.lock", str(cls.root / "deploy.lock"))
        )

    @classmethod
    def _install_scripts(cls, text):
        for command, marker in (
            ("aws-bank-container-run", "RUN_SCRIPT"),
            ("aws-bank-wait-healthy", "HEALTH_SCRIPT"),
            ("aws-bank-deploy", "DEPLOY_SCRIPT"),
        ):
            path = cls.bin / command
            path.write_text(cls._sandbox(cls._extract(text, command, marker)))
            path.chmod(0o700)

    @classmethod
    def _write_mocks(cls):
        (cls.bin / "aws").write_text("#!/bin/sh\necho token\n")
        (cls.bin / "mountpoint").write_text("#!/bin/sh\nexit 0\n")
        (cls.bin / "systemctl").write_text("#!/bin/sh\nexit 0\n")
        (cls.bin / "docker").write_text(
            "#!/bin/sh\n"
            "case \"$1\" in\n"
            "  login|pull) sleep \"${MOCK_SLEEP:-0}\"; exit 0 ;;\n"
            "  image) exit 0 ;;\n"
            "  rm) exit 0 ;;\n"
            "  run) status=$(sed -n '1p' \"$MOCK_STATE/sequence\" 2>/dev/null || echo healthy); "
            "printf '%s\\n' \"$status\" > \"$MOCK_STATE/health\"; "
            "sed -n '2,$p' \"$MOCK_STATE/sequence\" 2>/dev/null > \"$MOCK_STATE/sequence.next\" || true; "
            "mv -f \"$MOCK_STATE/sequence.next\" \"$MOCK_STATE/sequence\" 2>/dev/null || true; exit 0 ;;\n"
            "  inspect) cat \"$MOCK_STATE/health\" 2>/dev/null || echo healthy; exit 0 ;;\n"
            "esac\nexit 0\n"
        )
        for path in cls.bin.iterdir():
            path.chmod(0o700)

    def setUp(self):
        for path in self.data.glob("*"):
            path.unlink()
        for path in self.state.glob("*"):
            path.unlink()
        self.current = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/aws-bank@sha256:" + "1" * 64
        self.target = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/aws-bank@sha256:" + "2" * 64
        self.third = "123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/aws-bank@sha256:" + "3" * 64
        (self.data / "runtime.env").write_text("synthetic=1\n")
        (self.data / "image-uri").write_text(self.current + "\n")

    def run_helper(self, *args, **extra):
        env = os.environ.copy()
        env["PATH"] = str(self.bin) + os.pathsep + env["PATH"]
        env["MOCK_STATE"] = str(self.state)
        env.update(extra)
        return subprocess.run(
            ["bash", str(self.bin / "aws-bank-deploy"), *args],
            text=True,
            capture_output=True,
            env=env,
        )

    def test_success_promotes_only_after_healthy_replacement(self):
        (self.state / "sequence").write_text("healthy\n")
        result = self.run_helper("--image-uri", self.target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.data / "image-uri").read_text().strip(), self.target)
        self.assertEqual((self.data / "image-uri.previous").read_text().strip(), self.current)
        self.assertIn("independently reported healthy", result.stderr)

    def test_unhealthy_replacement_successful_rollback_is_failure(self):
        (self.state / "sequence").write_text("unhealthy\nhealthy\n")
        result = self.run_helper("--image-uri", self.target)
        self.assertEqual(result.returncode, 1)
        self.assertEqual((self.data / "image-uri").read_text().strip(), self.current)
        self.assertIn("rollback to last known-good image succeeded", result.stderr)

    def test_failed_rollback_has_distinct_failure_exit(self):
        (self.state / "sequence").write_text("unhealthy\nunhealthy\n")
        result = self.run_helper("--image-uri", self.target)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.data / "image-uri").read_text().strip(), self.current)
        self.assertIn("rollback to last known-good image FAILED", result.stderr)

    def test_concurrent_deployment_is_rejected_nonblocking(self):
        (self.state / "sequence").write_text("healthy\nhealthy\n")
        env = os.environ.copy()
        env["PATH"] = str(self.bin) + os.pathsep + env["PATH"]
        env["MOCK_STATE"] = str(self.state)
        env["MOCK_SLEEP"] = "2"
        first = subprocess.Popen(
            ["bash", str(self.bin / "aws-bank-deploy"), "--image-uri", self.target],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        time.sleep(0.2)
        second = self.run_helper("--image-uri", self.third)
        first_out, first_err = first.communicate(timeout=10)
        first_rc = first.returncode
        self.assertEqual(second.returncode, 75, second.stderr)
        self.assertEqual(first_rc, 0, first_err)


if __name__ == "__main__":
    unittest.main()
