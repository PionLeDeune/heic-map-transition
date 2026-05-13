import unittest
from pathlib import Path
import subprocess
import json

class TestScanHEIC(unittest.TestCase):

    def setUp(self):
        self.test_folder = Path("test_folder")
        self.test_folder.mkdir(exist_ok=True)
        self.test_file = self.test_folder / "test.heic"
        # Create a dummy HEIC file for testing
        with open(self.test_file, 'wb') as f:
            f.write(b'\0')  # Placeholder for a HEIC file

    def tearDown(self):
        for item in self.test_folder.iterdir():
            item.unlink()
        self.test_folder.rmdir()

    def test_exiftool_installed(self):
        result = subprocess.run(["which", "exiftool"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "exiftool should be installed")

    def test_gps_extraction(self):
        # Simulate running the scan_heic.py script
        cmd = ["python", "src/scan_heic.py", str(self.test_folder)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "The script should run without errors")

        # Check if the CSV file was created
        csv_file = self.test_folder / "heic_gps_list.csv"
        self.assertTrue(csv_file.exists(), "CSV file should be created")

        # Check if the HTML map was created
        html_file = self.test_folder / "heic_gps_map.html"
        self.assertTrue(html_file.exists(), "HTML map should be created")

    def test_no_heic_files(self):
        empty_folder = Path("empty_folder")
        empty_folder.mkdir(exist_ok=True)
        cmd = ["python", "src/scan_heic.py", str(empty_folder)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "The script should run without errors even if no HEIC files are found")

if __name__ == "__main__":
    unittest.main()