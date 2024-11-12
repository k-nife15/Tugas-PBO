/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package zakatmallulang;

public class Donatur {
    private String nama;
    private double totalHarta;

    public Donatur(String nama, double totalHarta) {
        this.nama = nama;
        this.totalHarta = totalHarta;
    }

    public String getNama() {
        return nama;
    }

    public void setNama(String nama) {
        this.nama = nama;
    }

    public double getTotalHarta() {
        return totalHarta;
    }

    public void setTotalHarta(double totalHarta) {
        this.totalHarta = totalHarta;
    }

    public double hitungZakat() {
        double nisab = 2 * 5000;
        if (totalHarta >= nisab) {
            return totalHarta * 0.025;
        } else {
            return 0; 
        }
    }
}
