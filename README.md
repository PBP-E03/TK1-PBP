# TK1-PBP

#### Nama Anggota Kelompok:
1. Danniel - 2306152090
2. Joshua Elisha Shalom Soedarmintarto - 2306275001
3. Anita Khoirun Nisa - 2306152273
4. Athallah Wibowo - 2306275576
5. Nafisa Arrasyida - 2306226391

#### Deskripsi Aplikasi 
Nama: SteakHouse Sigma
Deskripsi: SteakHouse Sigma adalah sebuah website yang dirancang untuk membantu pengguna menemukan dan memilih steakhouse terbaik di Jakarta. Melalui SteakHouse Sigma, pengguna dapat mencari steakhouse berdasarkan lokasi, harga, rating, dan jenis menu yang ditawarkan. Selain itu, pengguna dapat membaca dan menulis ulasan, berdiskusi dengan komunitas pecinta steak di forum, serta melakukan reservasi langsung ke steakhouse pilihan mereka.

#### Modul
1. Modul Pencarian Steakhouse - [Nama Anggota]
- Pengguna dapat mencari steakhouse berdasarkan nama, lokasi, harga, rating, dan jenis menu.
- Menampilkan daftar steakhouse yang sesuai dengan kriteria pencarian.
- Menyediakan fitur filter dan sorting untuk memudahkan pencarian.

2. Modul Ulasan dan Rating - [Nama Anggota]
- Pengguna yang telah login dapat menulis ulasan dan memberikan rating pada steakhouse yang pernah dikunjungi.
- Ulasan dan rating akan ditampilkan pada halaman detail steakhouse.
- Memungkinkan pengguna untuk melihat ulasan terbaru dan terpopuler.

3. Modul Reservasi dan Pemesanan Produk - [Nama Anggota]
- Pengguna dapat melakukan reservasi meja secara online.
- Formulir reservasi mencakup input nama, tanggal, waktu, jumlah tamu, dan kontak.
- Pengguna dapat melakukan booking S
- Sistem akan mengkonfirmasi ketersediaan dan memberikan notifikasi kepada pengguna.

5. Modul Forum Diskusi - [Nama Anggota]
- Pengguna dapat berdiskusi dengan anggota lain mengenai topik seputar steakhouse, menu, dan pengalaman kuliner.
- Fitur meliputi pembuatan topik baru, komentar, dan like/dislike.
- Memfasilitasi interaksi dan pertukaran informasi antar pengguna.

6. Modul Tambah Steakhouse - [Nama Anggota]
- Pengguna tertentu (misalnya, admin atau kontributor terverifikasi) dapat menambahkan data steakhouse baru.
- Formulir penambahan mencakup nama steakhouse, alamat, menu, harga, jam operasional, dan foto.
- Data akan diverifikasi sebelum ditampilkan untuk memastikan keakuratan informasi.

#### Dataset
```
Dataset yang digunakan berasal dari Kaggle dengan judul "Steakhouse Jakarta". Dataset ini berisi informasi lengkap mengenai steakhouse yang ada di Jakarta, termasuk nama, lokasi, rating, harga, dan detail lainnya yang relevan untuk aplikasi SteakHouse Sigma.
```

#### Roles
1. Pengguna tidak login:
- Dapat mengakses dan melihat daftar steakhouse.
- Dapat membaca ulasan dan rating dari pengguna lain.
- Dapat melihat diskusi yang ada di forum tanpa dapat berpartisipasi.

2. Pengguna login:
- Memiliki semua akses yang dimiliki pengguna tidak login.
- Dapat menulis ulasan dan memberikan rating pada steakhouse setelah proses reservasi berakhir.
- Dapat berpartisipasi dalam forum diskusi (membuat topik baru dan berkomentar).
- Dapat melakukan reservasi tempat dan memesan steak secara online.
- Dapat melihat daftar reservasi yang telah dibuat atau masih berlangsung.
- Dapat melihat riwayat reservasi yang sudah dilakukan.
- Dapat menambahkan steakhouse baru dan menu (jika memiliki hak akses khusus).

3. Admin:
- Memiliki semua akses yang dimiliki pengguna login.
- Dapat mengelola data steakhouse (menambah, mengedit, menghapus).
- Dapat memoderasi forum dan ulasan (menghapus konten yang tidak sesuai).
- Dapat melihat dan mengelola data reservasi pengguna.
