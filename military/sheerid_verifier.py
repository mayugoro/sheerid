"""Program verifikasi Military SheerID untuk ChatGPT"""
import re
import random
import logging
import httpx
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

# Konfigurasi log
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# Daftar organisasi military
MILITARY_ORGANIZATIONS = [
    {"id": 4070, "name": "Army"},
    {"id": 4073, "name": "Air Force"},
    {"id": 4072, "name": "Navy"},
    {"id": 4071, "name": "Marine Corps"},
    {"id": 4074, "name": "Coast Guard"},
    {"id": 4544268, "name": "Space Force"},
]

# Daftar nama depan dan belakang
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald",
    "Mark", "Paul", "Steven", "Andrew", "Kenneth", "Joshua", "Kevin", "Brian",
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
    "Harris", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King"
]


class SheerIDVerifier:
    """Verifikator Military SheerID"""

    def __init__(self, verification_id: str):
        self.verification_id = verification_id
        self.device_fingerprint = self._generate_device_fingerprint()
        self.http_client = httpx.Client(timeout=30.0)

    def __del__(self):
        if hasattr(self, "http_client"):
            self.http_client.close()

    @staticmethod
    def _generate_device_fingerprint() -> str:
        """Generate random device fingerprint"""
        chars = '0123456789abcdef'
        return ''.join(random.choice(chars) for _ in range(32))

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        """Parse verification ID dari URL"""
        match = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def generate_name() -> Dict[str, str]:
        """Generate nama random"""
        return {
            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_NAMES)
        }

    @staticmethod
    def generate_birth_date() -> str:
        """Generate tanggal lahir (18-65 tahun yang lalu)"""
        days_ago = random.randint(18 * 365, 65 * 365)
        birth_date = datetime.now() - timedelta(days=days_ago)
        return birth_date.strftime("%Y-%m-%d")

    @staticmethod
    def generate_discharge_date() -> str:
        """Generate tanggal pensiun (1-20 tahun yang lalu)"""
        days_ago = random.randint(1 * 365, 20 * 365)
        discharge_date = datetime.now() - timedelta(days=days_ago)
        return discharge_date.strftime("%Y-%m-%d")

    @staticmethod
    def generate_email(first_name: str, last_name: str) -> str:
        """Generate email address"""
        domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
        number = random.randint(100, 999)
        return f"{first_name.lower()}.{last_name.lower()}{number}@{random.choice(domains)}"

    def _sheerid_request(
        self, method: str, url: str, body: Optional[Dict] = None
    ) -> Tuple[Dict, int]:
        """Kirim request ke SheerID API"""
        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = self.http_client.request(
                method=method, url=url, json=body, headers=headers
            )
            try:
                data = response.json()
            except Exception:
                data = {"error": response.text}
            return data, response.status_code
        except Exception as e:
            logger.error(f"SheerID request gagal: {e}")
            raise

    def verify(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        birth_date: str = None,
        discharge_date: str = None,
    ) -> Dict:
        """Eksekusi proses verifikasi military"""
        try:
            # Generate data jika tidak ada
            if not first_name or not last_name:
                name = self.generate_name()
                first_name = name["first_name"]
                last_name = name["last_name"]

            if not email:
                email = self.generate_email(first_name, last_name)
            if not birth_date:
                birth_date = self.generate_birth_date()
            if not discharge_date:
                discharge_date = self.generate_discharge_date()

            # Pilih random organisasi military
            organization = random.choice(MILITARY_ORGANIZATIONS)

            logger.info(f"Informasi veteran: {first_name} {last_name}")
            logger.info(f"Email: {email}")
            logger.info(f"Organisasi: {organization['name']}")
            logger.info(f"Tanggal lahir: {birth_date}")
            logger.info(f"Tanggal pensiun: {discharge_date}")
            logger.info(f"Verification ID: {self.verification_id}")

            # Langkah 1: Submit status military
            logger.info("Langkah 1/2: Submit status military (VETERAN)...")
            step1_body = {
                "status": "VETERAN"
            }

            step1_data, step1_status = self._sheerid_request(
                "POST",
                f"https://services.sheerid.com/rest/v2/verification/{self.verification_id}/step/collectMilitaryStatus",
                step1_body,
            )

            if step1_status != 200:
                logger.error(f"❌ Langkah 1 gagal (status code {step1_status}): {step1_data}")
                return {
                    "success": False,
                    "message": f"Langkah 1 gagal (status code {step1_status}): {step1_data}",
                }

            # Dapatkan submissionUrl dari response
            submission_url = step1_data.get("submissionUrl")
            if not submission_url:
                logger.error("❌ submissionUrl tidak ditemukan dalam response")
                return {
                    "success": False,
                    "message": "submissionUrl tidak ditemukan dalam response langkah 1",
                }

            logger.info(f"✅ Status military berhasil, currentStep: {step1_data.get('currentStep')}")

            # Langkah 2: Submit informasi pribadi
            logger.info("Langkah 2/2: Submit informasi pribadi veteran...")
            step2_body = {
                "firstName": first_name,
                "lastName": last_name,
                "birthDate": birth_date,
                "email": email,
                "phoneNumber": "",
                "organization": {
                    "id": organization["id"],
                    "name": organization["name"]
                },
                "dischargeDate": discharge_date,
                "locale": "en-US",
                "country": "US",
                "metadata": {
                    "marketConsentValue": False,
                    "refererUrl": "",
                    "verificationId": self.verification_id,
                    "flags": '{"doc-upload-considerations":"default","doc-upload-may24":"default","doc-upload-redesign-use-legacy-message-keys":false,"docUpload-assertion-checklist":"default","include-cvec-field-france-student":"not-labeled-optional","org-search-overlay":"default","org-selected-display":"default"}',
                    "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the privacy policy of the business from which I am seeking a discount, and I understand that my personal information will be shared with SheerID as a processor/third-party service provider in order for SheerID to confirm my eligibility for a special offer."
                }
            }

            step2_data, step2_status = self._sheerid_request(
                "POST",
                submission_url,
                step2_body,
            )

            if step2_status != 200:
                logger.error(f"❌ Verifikasi gagal (status code {step2_status}): {step2_data}")
                return {
                    "success": False,
                    "message": f"Langkah 2 gagal (status code {step2_status}): {step2_data}",
                }

            # Cek apakah ada redirect URL
            redirect_url = step2_data.get("redirectUrl")
            current_step = step2_data.get("currentStep")

            if current_step == "success" or redirect_url:
                logger.info("✅ Verifikasi berhasil!")
                return {
                    "success": True,
                    "redirect_url": redirect_url,
                    "message": "Verifikasi military berhasil",
                    "data": step2_data,
                }
            elif current_step == "pending":
                logger.info("⏳ Dokumen menunggu review manual")
                return {
                    "success": True,
                    "pending": True,
                    "message": "Dokumen telah disubmit, menunggu review",
                    "data": step2_data,
                }
            elif current_step == "emailLoop":
                logger.info("📧 Perlu verifikasi email")
                return {
                    "success": True,
                    "pending": True,
                    "message": "Silakan cek email untuk verifikasi. Setelah klik link di email, verifikasi akan selesai.",
                    "data": step2_data,
                }
            else:
                logger.warning(f"⚠️ Status tidak jelas: {current_step}")
                return {
                    "success": False,
                    "message": f"Status verifikasi tidak jelas: {current_step}",
                    "data": step2_data,
                }

        except Exception as e:
            logger.error(f"Exception saat verifikasi: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
            }
