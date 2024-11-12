/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package zakatmallulang;

public class Penerima {
    private String nama;
    private String kategori;

    public Penerima(String nama, String kategori) {
        this.nama = nama;
        this.kategori = kategori;
    }

    public String getNama() {
        return nama;
    }

    public void setNama(String nama) {
        this.nama = nama;
    }

    public String getKategori() {
        return kategori;
    }

    public void setKategori(String kategori) {
        this.kategori = kategori;
    }

    public void tampilkanInfo() {
        System.out.println("Nama Penerima: " + nama);
        System.out.println("Kategori: " + kategori);
    }
}
