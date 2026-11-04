Nama : Athifah Mufidah
NPM : 2506612045
Kelas : PBP E

### Tugas 1

1. Ya, saya menggunakan elemen semantik HTML5 seperti <section> untuk membuat tampilan web menjadi lebih rapi dan teroganisir
2. Ketika mengatur tata letak elemen di web saya memperioritaskan foto profil dan section lain agar tidak tertumpuk
3. Karena saat ini web masih berbentuk static, saya  merasa bahwa web saya sedikit kosong. Kedepannya saya ingin membuat web ini menjadi lebih interaktif.

### Tugas 2

1. Saat lama certification diakses, request masuk ke urls.py proyek,
   diteruskan ke main/urls.py yang mencocokkan path ke named route
   show_certification, lalu memanggil view show_certification. View mengambil
   data lewat Certification.objects.all(), memasukkannya ke context, dan
   me-render template certification.html. Template menampilkan data lewat
   {% for %} dan pesan kondisi kosong lewat {% empty %} jika belum ada data.

2. Data disimpan di model, bukan hardcode di template, supaya data bisa
   ditambah/diubah/dihapus lewat database atau admin tanpa mengedit kode.
   Ini memisahkan tanggung jawab data (model) dan tampilan (template),
   sehingga aplikasi lebih mudah dipelihara dan dikembangkan.

3. makemigrations membaca perubahan di models.py dan membuat file migrasi,
   tanpa menyentuh database. migrate menerapkan file migrasi tersebut ke
   database. 
