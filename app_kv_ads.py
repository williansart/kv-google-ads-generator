import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from io import BytesIO

st.set_page_config(page_title="Gerador de Anúncios Google Ads com KV", layout="centered")
st.title("🧠 Geração de Anúncios Google Ads a partir de um KV")

st.markdown("Você pode **enviar um KV como imagem** ou **inserir manualmente os textos** abaixo para gerar anúncios formatados.")

modo = st.radio("Como você quer gerar o anúncio?", ["Enviar imagem (KV)", "Preencher manualmente"])

# Função para gerar imagem com o anúncio
def gerar_imagem_anuncio(titulo1, titulo2, descricao, chamada):
    largura = 800
    altura = 400
    fundo = Image.new("RGB", (largura, altura), color=(245, 245, 245))
    draw = ImageDraw.Draw(fundo)

    try:
        fonte_titulo = ImageFont.truetype("arial.ttf", 24)
        fonte_desc = ImageFont.truetype("arial.ttf", 20)
    except:
        fonte_titulo = fonte_desc = None  # fallback

    draw.text((30, 30), f"Título 1: {titulo1}", fill="black", font=fonte_titulo)
    draw.text((30, 80), f"Título 2: {titulo2}", fill="black", font=fonte_titulo)
    draw.text((30, 140), f"Descrição: {descricao}", fill="black", font=fonte_desc)
    draw.text((30, 200), f"Chamada (CTA): {chamada}", fill="blue", font=fonte_desc)

    return fundo

if modo == "Enviar imagem (KV)":
    img_file = st.file_uploader("📷 Envie seu KV (PNG ou JPG)", type=["png", "jpg", "jpeg"])
    if img_file:
        imagem = Image.open(img_file)
        st.image(imagem, caption="KV recebido", use_column_width=True)

        texto_extraido = pytesseract.image_to_string(imagem)
        st.subheader("🧾 Texto extraído do KV:")
        st.text_area("Texto OCR:", value=texto_extraido, height=150)

        if st.button("Gerar anúncio com base no KV"):
            linhas = texto_extraido.strip().splitlines()
            linhas = [l.strip() for l in linhas if l.strip()]
            t1 = linhas[0] if len(linhas) > 0 else "Título Exemplo"
            t2 = linhas[1] if len(linhas) > 1 else "Subtítulo Exemplo"
            desc = linhas[2] if len(linhas) > 2 else "Descrição breve do anúncio"
            cta = linhas[3] if len(linhas) > 3 else "Acesse agora"

            imagem_anuncio = gerar_imagem_anuncio(t1, t2, desc, cta)
            st.image(imagem_anuncio, caption="Anúncio Gerado")

            buffer = BytesIO()
            imagem_anuncio.save(buffer, format="PNG")
            buffer.seek(0)

            st.download_button("📥 Baixar Anúncio como PNG", buffer, file_name="anuncio_googleads.png", mime="image/png")

else:
    with st.form("manual_form"):
        t1 = st.text_input("Título 1 (até 30 caracteres)", max_chars=30)
        t2 = st.text_input("Título 2 (até 30 caracteres)", max_chars=30)
        desc = st.text_input("Descrição (até 90 caracteres)", max_chars=90)
        cta = st.text_input("Chamada/CTA", max_chars=60)
        submitted = st.form_submit_button("Gerar anúncio")

    if submitted:
        imagem_anuncio = gerar_imagem_anuncio(t1, t2, desc, cta)
        st.image(imagem_anuncio, caption="Anúncio Gerado")

        buffer = BytesIO()
        imagem_anuncio.save(buffer, format="PNG")
        buffer.seek(0)

        st.download_button("📥 Baixar Anúncio como PNG", buffer, file_name="anuncio_googleads.png", mime="image/png")