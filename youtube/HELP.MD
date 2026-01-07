Link YouTube agak berbeda, mirip dengan https://offers.sheerid.com/youtube/student/?yrdup=https%3A%2F%2Fwww.youtube.com%2F%3Fsld%3Dxxxxxxxxxxxxxxxytpid=premium&ytsku=premium&yrsp=https%3A%2F%2Fwww.youtube.com%2Fpremium%2FstudxxxxxxxxxxxxQQBRgO&euid=230493635&locale=en-US&oid=AI97cxxxxxxxxxxxxxxxxxxxxxNT06Nb5kDzo384b8cAu

Tidak ada informasi programId dan verificationId SheerID, jadi perlu capture sendiri interface-nya

Buka network log dan cari `https://services.sheerid.com/rest/v2/verification/`
Ambil programId dari payload dan verificationId dari response

Buat link manual
https://services.sheerid.com/verify/xxxxxxxxxx/?verificationId=yyyyyyyyyyy
xxx di sini adalah programId
yyyy adalah verificationId