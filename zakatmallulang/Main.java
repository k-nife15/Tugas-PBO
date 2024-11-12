/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package zakatmallulang;

import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<Penerima> daftarPenerima = new ArrayList<>();

        daftarPenerima.add(new Penerima("Budi", "Fakir Miskin"));
        daftarPenerima.add(new Penerima("Tono", "Amil Zakat"));
        daftarPenerima.add(new Penerima("Joko", "Ibnu Sabil"));
        daftarPenerima.add(new Penerima("Sabil", "Gharim"));
        
        System.out.println("Berapa kalikah anda ingin menghitung zakat mall?");
        int perulangan = input.nextInt();
        input.nextLine();

        for (int i = 0; i < perulangan; i++) {
            System.out.println("Masukkan nama Donatur: ");
            String namaDonatur = input.nextLine();

            System.out.println("Masukkan jumlah harta yang dimiliki: ");
            double totalHarta = input.nextDouble();
            input.nextLine();
            
            Donatur donatur = new Donatur(namaDonatur, totalHarta);
            double zakat = donatur.hitungZakat();

            if (zakat > 0) {
                System.out.println("Nama: " + donatur.getNama());
                System.out.println("Jumlah zakat yang harus dibayarkan sebesar = Rp." + zakat);
            } else {
                System.out.println("Mohon maaf, jumlah harta " + donatur.getNama() + " tidak memenuhi syarat untuk membayar Zakat mall.");
            }

            System.out.println("-----------------------------");
        }

        System.out.println("Apakah beberapa nama daftar penerima Zakat Mall? (y/n)");
        String pilihan = input.nextLine();
        
        if (pilihan.equalsIgnoreCase("y")) {
            System.out.println("Daftar Penerima Zakat:");
            for (Penerima penerima : daftarPenerima) {
                penerima.tampilkanInfo();
                System.out.println("-----------------------------");
            }
        }
        
        System.out.println("Program selesai.");
    }
}
