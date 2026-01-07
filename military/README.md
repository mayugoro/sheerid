# ChatGPT Military SheerID Ide Verifikasi

## 📋 Ringkasan

Proses verifikasi military ChatGPT berbeda dengan verifikasi mahasiswa/guru biasa, perlu eksekusi interface tambahan dulu untuk mengumpulkan informasi status military, lalu submit form informasi pribadi.

## 🔄 Alur Verifikasi

### Langkah 1: Kumpulkan Status Military (collectMilitaryStatus)

Sebelum submit form informasi pribadi, harus panggil interface ini dulu untuk set status military.

**Informasi Request**:
- **URL**: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectMilitaryStatus`
- **Method**: `POST`
- **Parameter**:
```json
{
    "status": "VETERAN" // Total 3
}
```

**Contoh Response**:
```json
{
    "verificationId": "{verification_id}",
    "currentStep": "collectInactiveMilitaryPersonalInfo",
    "errorIds": [],
    "segment": "military",
    "subSegment": "veteran",
    "locale": "en-US",
    "country": null,
    "created": 1766539517800,
    "updated": 1766540141435,
    "submissionUrl": "https://services.sheerid.com/rest/v2/verification/{verification_id}/step/collectInactiveMilitaryPersonalInfo",
    "instantMatchAttempts": 0
}
```

**Field Penting**:
- `submissionUrl`: URL submit yang perlu digunakan langkah berikutnya
- `currentStep`: Langkah saat ini, seharusnya berubah jadi `collectInactiveMilitaryPersonalInfo`

---

### Langkah 2: Kumpulkan Informasi Pribadi Military Non-Aktif (collectInactiveMilitaryPersonalInfo)

Gunakan `submissionUrl` yang dikembalikan langkah 1 untuk submit informasi pribadi.

**Informasi Request**:
- **URL**: Dapatkan dari `submissionUrl` response langkah 1
  - Contoh: `https://services.sheerid.com/rest/v2/verification/{verificationId}/step/collectInactiveMilitaryPersonalInfo`
- **Method**: `POST`
- **Parameter**:
```json
{
    "firstName": "name",
    "lastName": "name",
    "birthDate": "1939-12-01",
    "email": "your mail",
    "phoneNumber": "",
    "organization": {
        "id": 4070,
        "name": "Army"
    },
    "dischargeDate": "2025-05-29",
    "locale": "en-US",
    "country": "US",
    "metadata": {
        "marketConsentValue": false,
        "refererUrl": "",
        "verificationId": "",
        "flags": "{\"doc-upload-considerations\":\"default\",\"doc-upload-may24\":\"default\",\"doc-upload-redesign-use-legacy-message-keys\":false,\"docUpload-assertion-checklist\":\"default\",\"include-cvec-field-france-student\":\"not-labeled-optional\",\"org-search-overlay\":\"default\",\"org-selected-display\":\"default\"}",
        "submissionOptIn": "By submitting the personal information above, I acknowledge that my personal information is being collected under the <a target=\"_blank\" rel=\"noopener noreferrer\" class=\"sid-privacy-policy sid-link\" href=\"https://openai.com/policies/privacy-policy/\">privacy policy</a> of the business from which I am seeking a discount, and I understand that my personal information will be shared with SheerID as a processor/third-party service provider in order for SheerID to confirm my eligibility for a special offer. Contact OpenAI Support for further assistance at support@openai.com"
    }
}
```

**Penjelasan Field Penting**:
- `firstName`: Nama depan
- `lastName`: Nama belakang
- `birthDate`: Tanggal lahir, format `YYYY-MM-DD`
- `email`: Alamat email
- `phoneNumber`: Nomor telepon (bisa kosong)
- `organization`: Informasi organisasi militer (lihat daftar organisasi di bawah)
- `dischargeDate`: Tanggal pensiun, format `YYYY-MM-DD`
- `locale`: Region bahasa, default `en-US`
- `country`: Kode negara, default `US`
- `metadata`: Informasi metadata (termasuk teks persetujuan kebijakan privasi dll)

---

## 🎖️ Daftar Organisasi Militer (Organization)

Berikut adalah opsi organisasi militer yang tersedia:

```json
[
    {
        "id": 4070,
        "idExtended": "4070",
        "name": "Army",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4073,
        "idExtended": "4073",
        "name": "Air Force",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4072,
        "idExtended": "4072",
        "name": "Navy",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4071,
        "idExtended": "4071",
        "name": "Marine Corps",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4074,
        "idExtended": "4074",
        "name": "Coast Guard",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    },
    {
        "id": 4544268,
        "idExtended": "4544268",
        "name": "Space Force",
        "country": "US",
        "type": "MILITARY",
        "latitude": 39.7837304,
        "longitude": -100.445882
    }
]
```

**Mapping ID Organisasi**:
- `4070` - Army (Angkatan Darat)
- `4073` - Air Force (Angkatan Udara)
- `4072` - Navy (Angkatan Laut)
- `4071` - Marine Corps (Korps Marinir)
- `4074` - Coast Guard (Penjaga Pantai)
- `4544268` - Space Force (Angkatan Luar Angkasa)

---

## 🔑 Poin-Poin Implementasi

1. **Harus dieksekusi berurutan**: Harus panggil `collectMilitaryStatus` dulu, setelah dapat `submissionUrl`, baru panggil `collectInactiveMilitaryPersonalInfo`
2. **Informasi organisasi**: Field `organization` perlu berisi `id` dan `name`, bisa pilih random dari daftar di atas atau biarkan user pilih
3. **Format tanggal**: `birthDate` dan `dischargeDate` harus gunakan format `YYYY-MM-DD`
4. **Metadata**: `submissionOptIn` di field `metadata` berisi teks persetujuan kebijakan privasi, perlu extract dari request asli atau konstruksi

---

## 📝 Fitur Yang Perlu Diimplementasi

- [ ] Implementasi pemanggilan interface `collectMilitaryStatus`
- [ ] Implementasi pemanggilan interface `collectInactiveMilitaryPersonalInfo`
- [ ] Tambah logika pemilihan organisasi militer
- [ ] Generate informasi pribadi sesuai persyaratan (nama, tanggal lahir, email dll)
- [ ] Generate tanggal pensiun (perlu rentang waktu yang wajar)
- [ ] Handle informasi metadata (extract dari request asli atau konstruksi)
- [ ] Integrasi ke sistem command bot utama (seperti `/verify6`)

