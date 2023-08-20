PGDMP     #                    z         
   tugasanvis    14.2    14.2                 0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16489 
   tugasanvis    DATABASE     j   CREATE DATABASE tugasanvis WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_Indonesia.1252';
    DROP DATABASE tugasanvis;
                postgres    false            �            1259    16491    karyawan    TABLE       CREATE TABLE public.karyawan (
    id_karyawan integer NOT NULL,
    nama_depan character varying(30) NOT NULL,
    nama_belakang character varying(30) NOT NULL,
    jabatan character varying(30) NOT NULL,
    lama_bekerja character varying(30) NOT NULL
);
    DROP TABLE public.karyawan;
       public         heap    postgres    false            �            1259    16490    karyawan_id_karyawan_seq    SEQUENCE     �   CREATE SEQUENCE public.karyawan_id_karyawan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.karyawan_id_karyawan_seq;
       public          postgres    false    210                       0    0    karyawan_id_karyawan_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.karyawan_id_karyawan_seq OWNED BY public.karyawan.id_karyawan;
          public          postgres    false    209            �            1259    16505 	   pelanggan    TABLE     �   CREATE TABLE public.pelanggan (
    id_pelanggan integer NOT NULL,
    nama_pelanggan character varying(30) NOT NULL,
    nomor_kontak character varying(30) NOT NULL,
    email character varying(30) NOT NULL
);
    DROP TABLE public.pelanggan;
       public         heap    postgres    false            �            1259    16504    pelanggan_id_pelanggan_seq    SEQUENCE     �   CREATE SEQUENCE public.pelanggan_id_pelanggan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.pelanggan_id_pelanggan_seq;
       public          postgres    false    214                       0    0    pelanggan_id_pelanggan_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.pelanggan_id_pelanggan_seq OWNED BY public.pelanggan.id_pelanggan;
          public          postgres    false    213            �            1259    16498    produk    TABLE     �   CREATE TABLE public.produk (
    id_produk integer NOT NULL,
    nama_produk character varying(30) NOT NULL,
    kategori character varying(30) NOT NULL,
    harga character varying(30) NOT NULL
);
    DROP TABLE public.produk;
       public         heap    postgres    false            �            1259    16497    produk_id_produk_seq    SEQUENCE     �   CREATE SEQUENCE public.produk_id_produk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.produk_id_produk_seq;
       public          postgres    false    212                       0    0    produk_id_produk_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.produk_id_produk_seq OWNED BY public.produk.id_produk;
          public          postgres    false    211            �            1259    16512 	   transaksi    TABLE     >  CREATE TABLE public.transaksi (
    id_transaksi integer NOT NULL,
    tanggal_transaksi character varying(30) NOT NULL,
    id_pelanggan character varying(30) NOT NULL,
    id_produk character varying(30) NOT NULL,
    id_karyawan character varying(30) NOT NULL,
    total_pembelian character varying(30) NOT NULL
);
    DROP TABLE public.transaksi;
       public         heap    postgres    false            �            1259    16511    transaksi_id_transaksi_seq    SEQUENCE     �   CREATE SEQUENCE public.transaksi_id_transaksi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.transaksi_id_transaksi_seq;
       public          postgres    false    216                       0    0    transaksi_id_transaksi_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.transaksi_id_transaksi_seq OWNED BY public.transaksi.id_transaksi;
          public          postgres    false    215            k           2604    16494    karyawan id_karyawan    DEFAULT     |   ALTER TABLE ONLY public.karyawan ALTER COLUMN id_karyawan SET DEFAULT nextval('public.karyawan_id_karyawan_seq'::regclass);
 C   ALTER TABLE public.karyawan ALTER COLUMN id_karyawan DROP DEFAULT;
       public          postgres    false    209    210    210            m           2604    16508    pelanggan id_pelanggan    DEFAULT     �   ALTER TABLE ONLY public.pelanggan ALTER COLUMN id_pelanggan SET DEFAULT nextval('public.pelanggan_id_pelanggan_seq'::regclass);
 E   ALTER TABLE public.pelanggan ALTER COLUMN id_pelanggan DROP DEFAULT;
       public          postgres    false    214    213    214            l           2604    16501    produk id_produk    DEFAULT     t   ALTER TABLE ONLY public.produk ALTER COLUMN id_produk SET DEFAULT nextval('public.produk_id_produk_seq'::regclass);
 ?   ALTER TABLE public.produk ALTER COLUMN id_produk DROP DEFAULT;
       public          postgres    false    211    212    212            n           2604    16515    transaksi id_transaksi    DEFAULT     �   ALTER TABLE ONLY public.transaksi ALTER COLUMN id_transaksi SET DEFAULT nextval('public.transaksi_id_transaksi_seq'::regclass);
 E   ALTER TABLE public.transaksi ALTER COLUMN id_transaksi DROP DEFAULT;
       public          postgres    false    215    216    216                      0    16491    karyawan 
   TABLE DATA           a   COPY public.karyawan (id_karyawan, nama_depan, nama_belakang, jabatan, lama_bekerja) FROM stdin;
    public          postgres    false    210   �$                 0    16505 	   pelanggan 
   TABLE DATA           V   COPY public.pelanggan (id_pelanggan, nama_pelanggan, nomor_kontak, email) FROM stdin;
    public          postgres    false    214   �%                 0    16498    produk 
   TABLE DATA           I   COPY public.produk (id_produk, nama_produk, kategori, harga) FROM stdin;
    public          postgres    false    212   �&       	          0    16512 	   transaksi 
   TABLE DATA           {   COPY public.transaksi (id_transaksi, tanggal_transaksi, id_pelanggan, id_produk, id_karyawan, total_pembelian) FROM stdin;
    public          postgres    false    216   �'                  0    0    karyawan_id_karyawan_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.karyawan_id_karyawan_seq', 14, true);
          public          postgres    false    209                       0    0    pelanggan_id_pelanggan_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.pelanggan_id_pelanggan_seq', 13, true);
          public          postgres    false    213                       0    0    produk_id_produk_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.produk_id_produk_seq', 15, true);
          public          postgres    false    211                       0    0    transaksi_id_transaksi_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.transaksi_id_transaksi_seq', 31, true);
          public          postgres    false    215            p           2606    16496    karyawan karyawan_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.karyawan
    ADD CONSTRAINT karyawan_pkey PRIMARY KEY (id_karyawan);
 @   ALTER TABLE ONLY public.karyawan DROP CONSTRAINT karyawan_pkey;
       public            postgres    false    210            t           2606    16510    pelanggan pelanggan_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.pelanggan
    ADD CONSTRAINT pelanggan_pkey PRIMARY KEY (id_pelanggan);
 B   ALTER TABLE ONLY public.pelanggan DROP CONSTRAINT pelanggan_pkey;
       public            postgres    false    214            r           2606    16503    produk produk_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.produk
    ADD CONSTRAINT produk_pkey PRIMARY KEY (id_produk);
 <   ALTER TABLE ONLY public.produk DROP CONSTRAINT produk_pkey;
       public            postgres    false    212            v           2606    16517    transaksi transaksi_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.transaksi
    ADD CONSTRAINT transaksi_pkey PRIMARY KEY (id_transaksi);
 B   ALTER TABLE ONLY public.transaksi DROP CONSTRAINT transaksi_pkey;
       public            postgres    false    216               �   x�M�Ar�0E�_���(ܠ�����dd&��δ3e���zr@f�{Q�U]b�aC$��Rzt�K��ű�-��hz2�x~���C�"VPؐ�I��ytli��j����yaL>^瘵������{��q�+!JJ��i.������϶���Zᤂ$�\�v������
��S�
���j��Z�K7<�]���j]�>
��.�Z����n1�����ֆND���oC         Q  x�M�K�� @�x
N@M7�f7�M���U�$��O��b#e?^�Pϐǐ�+�Z��B��ܙY��x��0�T��5h�<�(�? :�7%^]��c$}��Ey^r��E�E+�|H�82'�gN'��iI�ۃXz\��a%zuyD�&S:Q��9)�y�n%�C*�UN)�r�G��(��i�̬��:E�0ʟ�I��Ԉ�E@����*�W��o=9�\:tb  ��,a��,-�)R�ᰵ2t�wf
�4�Rwi�-���Ӣ��I�Vd>��@�4%U��Lx�ґm;����B�h�X�(�S)���,6bVR[VQ�?YF&=���d��[��!��J�1M�����.         �   x�m�K� ���p
.��
�e�2��Tc��iM���تw����s�����{��Q��\�D����>�8T�ǋ&���O�>���\�� d������͠�d	W�0p�e6��c�LK�2S��T����F,�L,�*¬����4�\2崟sޢe2[˿�����]L�Џ}A�G��o,��j�������~��z�`X      	     x�URK1[��h�~����a�V�s13	M���>�i�LTL�h��X�&Ԉ��A]�����a(�K�vЎ�����p�,�x=� �Da���1
�sݖ}�`�
��F6|s*S2&�A�n��p�x��u��_:5���xR���V�v����jg�P�Fb�y�?�������͸a.W�A��%!�sf��� d�U�f,ݠZ��Y6e�"&�TgS�/ƃ����-&�b�"@��$���ig�qf_���9��"QF�Mw��9_�R��v�     