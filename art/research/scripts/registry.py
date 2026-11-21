"""Source registry for the art study (Prismfall). Every downloaded study image -> artist, page, image URL.
Downloads live in /home/claude/ref/art_refs/<source>/ (untracked, untrusted data). Game references are local read-only paths.
python3 -I registry.py  -> writes art/research/sources_registry.tsv"""
import os
R = '/home/claude/ref/art_refs'
SQ = 'https://images.squarespace-cdn.com/content/v1/6615412b7dfb903c456ec904/'
VG = 'https://storage.vgen.co/uploads/'
T = '-service-thumbnail-default'

HON = [l.split('\t') for l in '''v14_cover_art	0366c6a6-8070-4961-bd86-e8593b443f35/V14+Cover+art.png
juno_ref_portfolio	d054c366-b36a-4e32-98ca-dfd7d89aa982/Juno+ref+portfolio.png
damian_ref_sheet_v3	d4f3ff48-7808-4822-ba7e-05df60b9392b/Damian+ref+sheet+V3+twt.png
pom_ref_sheet_v3	3a441fb8-7027-46b0-a8c1-0592355a0e7f/Pom+ref+sheet+V3+twt.png
okarun_pixel	a17de418-3ea2-4b7f-8545-00d8abcbd2d8/okarun+pixel.png
momo_pixel	3014c0cb-7e01-4046-bc80-4f76101ca146/momo+pixel.png
rejuv_illust_bsky	4cf76dd3-a6a6-4970-ae76-a7247dbb1b4d/rejuv+illust+bsky.png
rejuv_illust	1f6b6f35-02c8-4c97-a079-a0e81a921fd4/rejuv+illust.png
rejuv_zine_1	151a8eed-1585-49f8-86ec-2345bb0e1028/rejuv+zine+1+wp.png
key_art_2021	9c3e3a68-bcbe-4cb5-91be-e6ed3568685f/2021+Key+Art+N+ARTSTATION.png
grief	ac5033fe-b3de-4a0c-9726-fdbbb373ea6a/Grief+WM.png
tarot_01_magician	94330b95-260c-48b7-b16c-c2d96fd772a8/01+The+Magician+bs.png
tarot_00_fool	321c690b-e437-49e8-ba59-8f9fa37390f2/00+The+Fool+bs.png
tarot_02_high_priestess	2ccda5f5-9e08-4e36-af8b-cf05cd0344b4/02+The+High+Priestess+bs.png
tarot_07_chariot	4c7e5c4b-f7fd-4259-a533-b13e2158a7b6/07+The+Chariot+bsky.png
amaria	813d1687-8e36-4757-94bc-7033861f25de/amaria+sm.png
contractual_obligations	7289b62f-5abb-4143-be5a-7ae51e18eb37/Contractual+Obligations+2021+WM.png
keep_running	23432595-99eb-44c7-bc12-9a3909b37cac/Keep+running+WM.png
big_illust	0aa8e51f-6032-4271-af6d-be3c517f0bd7/big+illust+wm.png
full_illust_penny	673348cd-52bc-46a7-8936-6b58e939fc14/full+illust+penny+twt.png
renegades	bb865f2e-b307-4737-a4b4-143cb7b87fda/renegades+WM.png
sunflowers	8d8eb49f-c49a-4551-9377-22a3c6fead97/sunflowers+twtr.png
illust_1	b1c55aaf-930d-47e7-9997-3c89cdf6c6b0/Illust+1+wm.png
illust_2	5a7693f8-c49c-4d13-bf14-4ac1f1909f7c/Illust+2+wm.png
full_illust	7a4a7c03-ebad-4c29-9936-ad5297c2e593/full+illust+wm.png
nyla_2024	b09ebfdf-5816-4cca-af6e-25c1f38d5b23/Nyla+%282024%29.png
warrior_full_illust	c5ecd9f5-19ab-44f1-a50d-4c0a67acd66b/Warrior+full+illust+twt.png
erin_wallpaper	3bb12f1f-5bf2-4db8-b5a4-64c4681f54cb/Erin+wallpaper+1440p.png
zumi_singlepage	9f7976fb-2a70-4bd4-8f1f-fdfa25110240/Zumi_Singlepage_twt.png
ryuki_zine	3cd92f82-929e-412d-a82c-d89c56fe7447/ryuki+zine+socmed.png
your_name_please_m3	6967c6fe-11cd-4118-a06e-97e9281cc9aa/Your+Name+Please+M3+Piece+TWT.png
aelita_wallpaper	bd46c5b9-a85a-47bb-a926-916e92bf09b0/Aelita+wallpaper+full.png'''.split('\n')]

VGEN = {
 'vgen_honnojis': ('Zumi / honnojis (VGen)', 'https://vgen.co/honnojis', 'df36b7de-cc42-4a19-8385-71a08ea34126', [
  ('bust_01', 'services/f6afeece-81d5-475f-9b88-6e8a97fc5d79'), ('bust_02', 'verified/FV75290IK2B7/88a8ea2a-d972-4b65-a549-cd5da09c1026'),
  ('bust_03', 'verified/8714WIVNX6TM/dc176bd4-9f51-4a4a-bfbc-2474f3ebcca1'), ('bust_04', 'verified/H7M1RFNWU0P7/e5795226-e1b2-4d3f-ba75-9e2047e42d6d'),
  ('bust_05', 'services/9976ad16-2a03-4956-8a85-c96faa672068'), ('bust_06', 'services/333bd210-b35a-4319-8618-af3a1ef7c7d0'),
  ('illust_07', 'services/6f1a2bd4-86ed-40cd-aab7-98466efc6acc'), ('illust_08', 'verified/JIMASUT7UN6C/735cb647-0487-4383-89b2-30475947df3b'),
  ('illust_09', 'services/f5a2fd38-8125-4436-a73f-d33fd92a2c37'), ('illust_10', 'services/f1f38617-668c-4fee-a758-5cb712cefbd4'),
  ('illust_11', 'services/9c5f2bce-7896-49f3-8653-3b1414a706a2'), ('illust_12', 'services/14a6ad72-a23a-4062-8c86-3b0b5e0dc3af'),
  ('chibi_13', 'services/ed21ef8b-b08f-417a-9ff9-8fcfc8e1086f'), ('chibi_14', 'verified/C3T28PYY7ICX/ab2e4b2d-60a4-404b-89c1-2831306b85d5'),
  ('chibi_15', 'verified/V2O0JJ5WX25R/cc970cd0-80a6-492a-bd45-4cb3e612e0a2'), ('chibi_16', 'verified/26CL998JGM9G/adbcd30c-8110-4dcc-bdda-d04d24a7011c'),
  ('chibi_17', 'services/423658fc-e0ea-473a-9ce7-38af0feae4b8'), ('chibi_18', 'services/e62983d8-c783-4d59-8ba2-e5abefaccdad')]),
 'vgen_angeceleste': ('angeceleste (VGen)', 'https://vgen.co/angeceleste/service/pokemon-trainer-sprite/bf1da690-dc41-4c38-bd47-7f5a53b1d3db', '9da71c4c-a02c-4308-8c5c-c3334287b502', [
  ('01', 'services/8cee67f1-b425-43a0-9281-851a33dba6cc', 'full'), ('02', 'services/c349b386-5880-439c-87b8-827271ae1c9d'),
  ('03', 'verified/L21L269MJWM/bbc4769a-9142-4530-afe4-324dd0906b61'), ('04', 'verified/JOVFG7IDLM9/7935c10d-be57-4b70-b74a-febf1960d7a4'),
  ('05', 'verified/HMQ4BRDSWHSB/ed31ec47-db8f-4367-86d9-1433fbc19934'), ('06', 'verified/HN7HR5TAV4TT/ebc13284-5092-4f29-b385-43036f85de04'),
  ('07', 'verified/GJESOXYG8I1H/fb7f3b69-8aea-4e2c-b177-214bd489f8cb'), ('08', 'services/0705d2cb-9d40-4d92-a393-85745da257ff')]),
 'vgen_silversrini': ('SilverSrini (VGen)', 'https://vgen.co/SilverSrini/service/pokemon-trainer/ddda7526-f492-46db-81fe-4724a035f81a', 'fd17009f-c84f-4d8a-9045-75434f5cf97c', [
  ('01', 'services/00637882-7e16-4d36-a0ff-c8054a9b2ea6', 'full'), ('02', 'services/e2fd1f05-5cee-40d3-b546-b4f36615f6dc'),
  ('03', 'services/b94a6f04-c525-40fb-a2c4-d17d4ee241ea'), ('04', 'services/e565d429-8129-4ea4-b41d-1b42158a88d7'),
  ('05', 'services/d21bd0fa-4432-4393-bdb2-f8d17b0e0b62')]),
 'vgen_princeloppy': ('Princeloppy (VGen)', 'https://vgen.co/Princeloppy/service/pokemon-style/6dc1c88b-dd62-4999-935e-222302d3081b', '449ea1b1-8481-48a5-b61b-898e0aa6a522', [
  ('01', 'services/397cc2e4-86d7-4f28-8338-faa8919a9b66', 'full'), ('02', 'services/593200a9-7b63-48c3-92c8-e38fe7ff1a4d'),
  ('03', 'services/5a20af28-553f-416a-a9ed-da7fee65c441'), ('04', 'services/3aece00f-7e1f-4d5c-965b-0d6ea057d331'),
  ('05', 'verified/QW9RL5G1M4QY/95246c19-76e7-4429-8b31-dba644c2d288'), ('06', 'verified/9H7TKB9L4EEE/409f4060-5d7b-4d14-bfb2-6057b44ac350'),
  ('07', 'verified/M5YYQON8GBT4/e4dd3b03-d549-4a94-b5ce-ce414b23d277'), ('08', 'verified/AN9VQ9M3ER2M/5fc8d164-525f-4724-8fb5-5f78ba57efb5'),
  ('09', 'services/f41a7b2e-7885-4662-84ef-3364b6434cb4'), ('10', 'services/e60dc543-f2ff-4172-b0dc-1e73a23923e0')]),
 'vgen_noodlesxl': ('NoodlesXL / r_ramenoodles (VGen)', 'https://vgen.co/r_ramenoodles/service/fields-of-mistria-inspired-character-portrait/b7f6e4a4-cac5-4983-8148-76de661b6bf0', '50e8f5e7-255e-4351-bc17-452e141d50f7', [
  ('01', 'services/9f3d1066-2c93-4de3-8ae2-fb09e7e054c9'), ('02', 'services/3748d627-4164-4ffd-bc52-469e439c91ec'),
  ('03', 'services/7b50e7fb-7d02-4a1a-b103-84f25db1adbc'), ('04', 'services/e271bf78-04d7-4bc5-ac4a-abcb1219f665'),
  ('05', 'services/54220fd1-7139-4bd1-b775-b51d49e7d30a'), ('06', 'services/2643ca64-752a-4113-a6e4-ae0f6709c36b'),
  ('07', 'services/dd7cfdf6-8ad4-4b73-9a6c-0da53c82ca45'), ('08', 'services/a4bd5393-310c-4b18-84f8-d9d2513cd0a4'),
  ('09', 'services/9f147644-39b6-458e-99de-e0df9716c5f7'), ('10', 'services/2f4bb607-2885-426b-ad86-8a8589db65bb'),
  ('11', 'services/44459c1d-ebec-4f2e-8069-af1d3ce8a897'), ('12', 'services/c10fc50b-de3b-454c-9e70-3f922d5f3635'),
  ('13', 'services/bde99712-7098-43cb-8874-66d7e1b127a7'), ('14', 'services/8140f1f6-dd32-44c0-95f2-be9bd9d3f384', 'webm')]),
 'vgen_mossgrover': ('Mossgrover (VGen)', 'https://vgen.co/Mossgrover/service/pixel-art-talking-sprite-64x64-/a0385791-daa5-4fcb-8984-e805144312bb', '7eba41ea-4fae-47c1-aa84-6486accd17f2', [
  ('01', 'services/ee0f5c44-8e48-486a-9582-314808b798f5', 'webm'), ('02', 'services/76977ee6-471d-41b2-8508-6b8898e8155a', 'webm'),
  ('03', 'services/81653d09-a273-4a8b-b1fb-17656a496ae9', 'webm'), ('04', 'services/7281d6b0-7468-4231-b629-7a9fb3b396fb', 'webm'),
  ('05', 'services/9bd20dac-3bb0-4fcd-8694-b1374f6ca06d', 'webm'), ('06', 'services/6377eb58-c7bb-417b-a92e-26aecbb5712b', 'webm')]),
 'vgen_inkyfrosty': ('InkyFrosty (VGen)', 'https://vgen.co/InkyFrosty/service/animated-pixel-portraits/ed136134-e853-46f4-8355-74b789a390cc', 'd776c622-c7b5-4675-94d6-08346199dab5', [
  ('01', 'services/3feacf78-76c7-4787-ab4f-5817b928b9f1', 'webm'), ('02', 'verified/YDLFO6ORSOIF/9bb3478a-4099-42a5-a6d2-b5675328ed18', 'webm'),
  ('03', 'verified/BWIQ6DGRPDY1/a44bcb60-e47e-4e0f-a3d8-769f479e6e59', 'webm'), ('04', 'verified/CYHDA7WY7J74/a59d2e57-acab-483c-9324-15643745dfb4', 'webm'),
  ('05', 'services/8c5282f6-946e-4792-a8c2-fdd3fa0079e0')]),
 'vgen_ngreentail': ('Nifast Greentail (VGen)', 'https://vgen.co/NGreentail', '2fa05b79-a3e5-40d1-8a8a-05ffa771ce31', [
  ('01', 'services/43c5a97d-ebe1-4ade-8e2c-b67c0b53413a'), ('02', 'verified/9V2QZUAXO5MA/a01b3363-4a20-4702-a286-4912d806e576'),
  ('03', 'verified/3C33EF95TMSD/697e9f82-ae7b-461f-a7a4-955650f9b786'), ('04', 'verified/JLHDNO803NVE/8b459f66-1002-4ff1-bfef-70a84260280f'),
  ('05', 'services/2d5e02ca-9dfa-4c72-83ea-2b6cbc90979f'), ('06', 'services/4e4213c3-a91a-4446-8688-a5d52c8187a4')]),
 'vgen_fiorne': ('Fiorne (VGen)', 'https://vgen.co/Fiorne', 'cd10f722-e003-401c-92ef-d2f0d5edbb95', [
  ('01', 'services/5f93f7f1-6c47-414e-8ae4-f58684b8d234'), ('02', 'verified/IM6CGBDUHFHE/47ce628b-20c4-41d7-ba2f-3dcd71a71ee7'),
  ('03', 'verified/W6NJYGFKLH5G/310d139a-0139-48de-a34e-d1f279e0e26b'), ('04', 'services/6fc8067f-47ae-4428-958e-56acb281c3ba'),
  ('05', 'services/9510b531-2c00-4ea7-80a0-9a39913810ac'), ('06', 'verified/BPJTQCTPTMBJ/55c20732-09c4-432b-8224-18ea7ae29d6b'),
  ('07', 'services/0a1be2cb-3098-49a3-88e2-a4dd39bbcfa5'), ('08', 'services/4fa8bd42-63e1-4c2e-b83c-5d3832730890')]),
}


def rows():
    out = []
    for n, p in HON:
        out.append((f'honnojis/{n}.png', 'Zumi / honnojis (official Pokemon Rejuvenation artist)', 'https://www.honnojis.art/', SQ + p))
    for src, (artist, page, base, items) in VGEN.items():
        for it in items:
            name, path = it[0], it[1]
            kind = it[2] if len(it) > 2 else 'thumb'
            url = VG + base + '/' + path + ('.webp' if kind == 'full' else (T + '.webm (frame)' if kind == 'webm' else T + '.webp'))
            out.append((f'{src}/{name}.png', artist, page, url))
    return [r for r in out if os.path.exists(os.path.join(R, r[0]))]


if __name__ == '__main__':
    rs = rows()
    with open('/home/claude/fangame/art/research/sources_registry.tsv', 'w') as f:
        f.write('local_file\tartist\tpage\timage_url\n')
        for r in rs: f.write('\t'.join(r) + '\n')
    print(len(rs), 'rows')
