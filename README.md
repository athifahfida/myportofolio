Nama : Athifah Mufidah
NPM : 2506612045
Kelas : PBP E

### Tugas 1
1. Ya, saya menggunakan elemen semantik HTML5 seperti <section> untuk membuat tampilan web menjadi lebih rapi dan teroganisir
2. Ketika mengatur tata letak elemen di web saya memperioritaskan foto profil dan section lain agar tidak tertumpuk
3. Karena saat ini web masih berbentuk static, saya  merasa bahwa web saya sedikit kosong. Kedepannya saya ingin membuat web ini menjadi lebih interaktif.

### Tugas 2
1. Saat lama certification diakses, request masuk ke urls.py proyek, diteruskan ke main/urls.py yang mencocokkan path ke named route show_certification, lalu         memanggil view show_certification. View mengambil data lewat Certification.objects.all(), memasukkannya ke context, dan me-render template certification.html.     Template menampilkan data lewat {% for %} dan pesan kondisi kosong lewat {% empty %} jika belum ada data.
2. Data disimpan di model, bukan hardcode di template, supaya data bisa ditambah/diubah/dihapus lewat database atau admin tanpa mengedit kode. Ini memisahkan         tanggung jawab data (model) dan tampilan (template), sehingga aplikasi lebih mudah dipelihara dan dikembangkan.
3. makemigrations membaca perubahan di models.py dan membuat file migrasi tanpa menyentuh database. migrate menerapkan file migrasi tersebut ke database. 


### Tugas 6
1. REST adalah gaya merancang API. Data dianggap sebagai resource dengan URL sendiri (misalnya /skills/<id>/) dan diakses lewat metode HTTP standar (GET, POST,       PUT, PATCH, DELETE. JSON saja belum cukup untuk disebut RESTful. API juga harus memakai URL berbasis resource, metode HTTP sesuai artinya, dan status HTTP         yang tepat (201, 204, 403, 404). API yang selalu membalas 200 OK dengan {"error":} memang berformat JSON, tetapi tidak RESTful. PUT mengganti seluruh data,        jadi semua field harus dikirim. PUT dipakai saat form edit mengirim semua field sekaligus. PATCH mengubah sebagian field saja dan dipakai saat hanya satu          field yang berubah.
2. Serializer mengubah objek model menjadi JSON, dan mengubah JSON dari client menjadi data yang sudah divalidasi. Keuntungannya dibanding JsonResponse manual:  
      -Daftar field ditulis sekali, tidak berulang di setiap view.  
      -Validasi otomatis (termasuk validate_<field> dan strip_tags), dan error 400 dibuat otomatis.  
      -Data sensitif tidak bocor karena field ditulis eksplisit.  
      -Field seperti star_count bisa dibuat read-only.  
3. Autentikasi menangani login lewat session. Otorisasi menangani permission. Menyembunyikan tombol hanya mengatur tampilan, bukan keamanan. Siapapun bisa            mengirim request langsung lewat Console atau Postman tanpa lewat tombol. Karena itu server harus memeriksa hak akses di setiap request.
4. Dengan SessionAuthentication, browser otomatis mengirim cookie session ke server. Situs jahat bisa memanfaatkannya untuk mengirim request atas nama user yang      sedang login. Token CSRF mencegah ini, karena situs jahat tidak bisa membaca token dan tidak bisa menyertakannya di header X-CSRFToken. Dengan                     SessionAuthentication, browser otomatis mengirim cookie session ke server. Situs jahat bisa memanfaatkannya untuk mengirim request atas nama user yang sedang      login. Token CSRF mencegah ini karena situs jahat tidak bisa membaca token dan tidak bisa menyertakannya di header X-CSRFToken.
