import streamlit as st
import pandas as pd
from io import BytesIO
import base64

# Konfigurasi halaman
st.set_page_config(page_title="Data Matching App", layout="wide")

# Fungsi untuk konversi dataframe ke Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.read()

# Fungsi untuk membuat link download
def get_table_download_link(df, filename, text):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">{text}</a>'

# Header aplikasi
st.title("Data Matching Application")
st.markdown("Upload two CSV files, remove duplicates, and match data based on selected columns.")

# Sidebar untuk upload file
with st.sidebar:
    st.header("Upload Data")
    st.subheader("First CSV File")
    file1 = st.file_uploader("Choose first CSV file", type=['csv'], key="file1")
    st.subheader("Second CSV File")
    file2 = st.file_uploader("Choose second CSV file", type=['csv'], key="file2")

# Main content
if file1 is not None and file2 is not None:
    try:
        try:
            df1 = pd.read_csv(file1)
        except UnicodeDecodeError:
            df1 = pd.read_csv(file1, encoding='latin1')
        
        try:
            df2 = pd.read_csv(file2)
        except UnicodeDecodeError:
            df2 = pd.read_csv(file2, encoding='latin1')

        # Tampilkan data awal
        st.subheader("Original Data Preview")
        col1, col2 = st.columns(2)

        with col1:
            st.write("First Dataset")
            st.write(f"Shape: {df1.shape}")
            st.dataframe(df1.head())

        with col2:
            st.write("Second Dataset")
            st.write(f"Shape: {df2.shape}")
            st.dataframe(df2.head())

        # Hapus duplikat
        st.subheader("Remove Duplicates")
        remove_duplicates = st.checkbox("Remove duplicates from both datasets", value=True)

        if remove_duplicates:
            df1_cleaned = df1.drop_duplicates()
            df2_cleaned = df2.drop_duplicates()
        else:
            df1_cleaned = df1.copy()
            df2_cleaned = df2.copy()

        # Tampilkan data setelah cleaning
        st.write("Data After Removing Duplicates")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"First Dataset (Shape: {df1_cleaned.shape})")
            st.dataframe(df1_cleaned.head())

        with col2:
            st.write(f"Second Dataset (Shape: {df2_cleaned.shape})")
            st.dataframe(df2_cleaned.head())

        # Pilihan kolom untuk matching
        st.subheader("Match Datasets")
        st.write("Select columns to match the datasets")

        col1, col2 = st.columns(2)

        with col1:
            key_col1 = st.selectbox("Select key column from first dataset", df1_cleaned.columns, key="key1")

        with col2:
            key_col2 = st.selectbox("Select key column from second dataset", df2_cleaned.columns, key="key2")

        join_type = st.selectbox("Select join type", ["inner", "left", "right", "outer"])

        # Tombol untuk mencocokkan
        if st.button("Match Datasets"):
            try:
                # Pastikan kolom key sama tipe datanya
                df1_cleaned[key_col1] = df1_cleaned[key_col1].astype(str)
                df2_cleaned[key_col2] = df2_cleaned[key_col2].astype(str)

                matched_df = pd.merge(
                    df1_cleaned,
                    df2_cleaned,
                    how=join_type,
                    left_on=key_col1,
                    right_on=key_col2,
                    suffixes=('_df1', '_df2')
                )

                st.subheader("Matched Result")
                st.write(f"Shape: {matched_df.shape}")
                st.dataframe(matched_df.head())

                # Download hasil
                st.markdown(
                    get_table_download_link(matched_df, 'matched_data.xlsx', '📥 Download matched data'),
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"❌ Error matching datasets: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error processing files: {str(e)}")
else:
    st.info("📂 Please upload both CSV files to begin.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Deployable to Streamlit Cloud")
