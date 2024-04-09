import streamlit as st
from aes import AES  
from rsa import generate_key_pair, encrypt, decrypt, split_message, split_blocks, join_blocks

st.markdown("""
    <style>
    .centered {
        text-align: center;
    }
    .stButton>button {
        display: block;
        margin: 0 auto;
    }
    .stTextArea>div>div {
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("Logo_IUH.png", use_column_width=True)

algorithm_choice = st.sidebar.selectbox('Chọn thuật toán:', ['AES', 'RSA'])

st.markdown(f'<h1 class="centered">MÃ HÓA {algorithm_choice}</h1>', unsafe_allow_html=True)


# Kiểm tra lựa chọn thuật toán và hiển thị giao diện tương ứng
if algorithm_choice == 'AES':
    # Định nghĩa tab
    tab1, tab2 = st.tabs(["Mã hóa", "Giải mã"])

    # Tab Mã hóa
    with tab1:
        key_encrypt = st.text_input('Nhập mã khóa:', max_chars=16, key="key_encrypt")
        if len(key_encrypt) != 16:
            st.error('Mã khóa cần có 16 ký tự.')
        plaintext = st.text_area('Nhập chuỗi cần mã hóa')
        if st.button('Mã hóa', key="encrypt"):
            aes = AES(int.from_bytes(key_encrypt.encode(), 'big'))
            encrypted_text = aes.encrypt(int.from_bytes(plaintext.encode(), 'big'))
            encrypted_text_hex = hex(encrypted_text)[2:] 
            st.text_area('Bản mã:', encrypted_text_hex, height=100)

    # Tab Giải mã
    with tab2:
        key_decrypt = st.text_input('Nhập mã khóa:', max_chars=16, key="key_decrypt")
        if len(key_decrypt) != 16:
            st.error('Mã khóa cần có 16 ký tự.')
        ciphertext_hex = st.text_area('Nhập chuỗi cần giải mã')
        if st.button('Giải mã', key="decrypt"):
            try:
                ciphertext_bytes = bytes.fromhex(ciphertext_hex)
                ciphertext_int = int.from_bytes(ciphertext_bytes, byteorder='big')
                aes = AES(int.from_bytes(key_decrypt.encode(), 'big'))
                decrypted_int = aes.decrypt(ciphertext_int)
                byte_length = (decrypted_int.bit_length() + 7) // 8 or 16
                decrypted_text = decrypted_int.to_bytes(byte_length, 'big').decode(errors='ignore').rstrip('\x00')
                st.text_area('Bản rõ', decrypted_text, height=100)
            except ValueError as e:
                st.error(f'Invalid input for decryption: {e}')
elif algorithm_choice == 'RSA':

    rsa_tab1, rsa_tab2 = st.tabs(["Mã hóa", "Giải mã"])
    if 'history' not in st.session_state:
        st.session_state.history = []

    uploaded_file = st.file_uploader('Tải lên tệp tin .txt', type='txt', key='file_upload_key')

    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    else:
        text = ''

    # Tab Mã hóa
    with rsa_tab1:
        p = st.text_input('Nhập số nguyên tố p:')
        q = st.text_input('Nhập số nguyên tố q:')
        message = st.text_area('Nhập thông điệp để mã hóa:', value=text)

        if st.button('Mã hóa'):
            try:
                p = int(p)
                q = int(q)
                public, private = generate_key_pair(p, q)
                block_size = len(str(public[1])) - 1
                blocks = split_message(message, block_size)
                encrypted_blocks = []
                for block in blocks:
                    encrypted_block = encrypt(public, block)
                    encrypted_blocks.extend(encrypted_block)
                encrypted_message = join_blocks(encrypted_blocks)
                st.write('Thông điệp đã được mã hóa:', encrypted_message)
                st.session_state.history.append({'mode': 'Encrypt', 'public_key': public, 'private_key': private, 'encrypted_message': encrypted_message})
            except ValueError as e:
                st.error(str(e))

    with rsa_tab2:
        encrypted_message_input = st.text_area('Nhập thông điệp đã mã hóa để giải mã:', value=text)
        d = st.text_input("Nhập private key 'd':")
        n = st.text_input("Nhập private key 'n':")

        if st.button('Giải mã'):
            try:
                d = int(d)
                n = int(n)
                private_key = (d, n)
                encrypted_blocks = split_blocks(encrypted_message_input)
                decrypted_message = decrypt(private_key, encrypted_blocks)
                st.write('Thông điệp đã được giải mã:', decrypted_message)
                st.session_state.history.append({'mode': 'Decrypt', 'private_key': private_key, 'encrypted_message': encrypted_message_input, 'decrypted_message': decrypted_message})
            except ValueError as e:
                st.error(str(e))

    # Hiển thị lịch sử ở giao diện chính và thêm nút xóa lịch sử
    st.header('Lịch sử')
    for index, entry in enumerate(st.session_state.history):
        st.subheader(f'Tác vụ {index + 1}')
        if entry['mode'] == 'Encrypt':
            st.write("Public key 'e':", entry['public_key'][0])
            st.write("Public key 'n':", entry['public_key'][1])
            st.write("Private key 'd':", entry['private_key'][0])
            st.write('Thông điệp đã được mã hóa:', entry['encrypted_message'])
        else:
            st.write("Private key 'd':", entry['private_key'][0])
            st.write('Thông điệp đã được mã hóa:', entry['encrypted_message'])
            st.write('Thông điệp đã được giải mã:', entry['decrypted_message'])

    if st.button('Xóa Lịch Sử'):
        st.session_state.history = []