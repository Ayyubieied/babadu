-- Fitria Dwi Cahya
-- 2106751410
-- Kelompok C11

 -- Update score peserta

CREATE OR REPLACE FUNCTION selesaikanPertandingan() 
RETURNS TRIGGER as 
$$ 
    DECLARE 
        poin INT;
        nomor_peserta VARCHAR(255);
        kategori_superseries VARCHAR(255);
        jenis_babak VARCHAR(255);
        
    BEGIN 
        IF (TG_OP = 'UPDATE' OR TG_OP = 'INSERT') THEN

              (SELECT pm.nomor_peserta AS nomor_peserta, pm.jenis_babak AS jenis_babak, v.kategori_superseries as kategori_superseries, pp.point as poin FROM PESERTA_MENGIKUTI_MATCH pm 
                JOIN MATCH m ON pm.jenis_babak = m.jenis_babak AND pm.tanggal = m.tanggal AND pm.waktu_mulai = m.waktu_mulai 
                JOIN EVENT v ON m.nama_event = v.nama_event AND m.tahun_event = v.tahun JOIN POINT_PERTANDINGAN pp ON pp.jenis_babak = pm.jenis_babak AND pp.kategori_superseries = v.kategori_superseries
                WHERE v.nama_event = NEW.nama_event AND v.tahun= NEW.tahun_event AND pm.status_menang = '0')
            UNION (SELECT pm.nomor_peserta AS nomor_peserta, pm.jenis_babak AS jenis_babak, v.kategori_superseries as kategori_superseries, pp.point as poin FROM FROM PESERTA_MENGIKUTI_MATCH pm 
                JOIN MATCH m ON pm.jenis_babak = m.jenis_babak AND pm.tanggal = m.tanggal AND pm.waktu_mulai = m.waktu_mulai 
                JOIN EVENT v ON m.nama_event = v.nama_event AND m.tahun_event = v.tahun JOIN POINT_PERTANDINGAN pp ON pp.jenis_babak = pm.jenis_babak AND pp.kategori_superseries = v.kategori_superseries
                WHERE v.nama_event = NEW.nama_event AND v.tahun= NEW.tahun_event AND pm.status_menang = '1' AND pm.jenis_babak = 'Final');

            SELECT ID_Atlet_Ganda FROM PESERTA_KOMPETISI WHERE nomor_peserta = nomor_peserta;
            SELECT ID_Atlet_Kualifikasi FROM PESERTA_KOMPETISI WHERE nomor_peserta = nomor_peserta;

            IF ID_Atlet_Ganda IS NOT NULL THEN 
                SELECT ID_Atlet_Kualifikasi, ID_Atlet_Kualifikasi_2 FROM ATLET_GANDA WHERE ID_Atlet_Ganda = ID_Atlet_Ganda;
                -- menambahkan point ke total point kedua orang atlet
                UPDATE TOTAL_POINT
                SET total_point = point + pointGames WHERE ID_Atlet = ID_Atlet_Kualifikasi;

                UPDATE atlet_kualifikasi
                SET world_rank = rank
                WHERE ID_Atlet = ID_Atlet_Kualifikasi;
                
            ELSE 
                UPDATE TOTAL_POINT
                SET total_point = point + pointGames WHERE ID_Atlet = ID_Atlet_Kualifikasi;
                UPDATE atlet_kualifikasi
                SET world_rank = rank
                WHERE ID_Atlet = ID_Atlet_Kualifikasi;
         END IF ;
            RETURN NEW;
        END IF;
    END
$$
LANGUAGE plpgsql;



CREATE TRIGGER triggerSelesaikanPertandingan
    BEFORE UPDATE OR INSERT ON PESERTA_MENGIKUTI_MATCH
    FOR EACH ROW
    EXECUTE PROCEDURE selesaikanPertandingan();