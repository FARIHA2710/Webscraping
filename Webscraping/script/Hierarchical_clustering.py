# from googletrans import Translator
# import pandas as pd
#
# translator = Translator()
#
# # Load your Excel file
# df = pd.read_excel('Datatest.xlsx', sheet_name='Sheet1')
#
# # Translate a single cell and handle exceptions
# def translate_cell(cell):
#     try:
#         # Translate the cell to English
#         return translator.translate(cell, dest='en').text
#     except Exception as e:
#         print(f"Error translating cell: {cell}, error: {e}")
#         return cell  # Return the original cell if translation fails
#
# # Create a new DataFrame for the translated content
# df_translated = pd.DataFrame()
#
# for column in df.columns:
#     # Apply the translate function to each cell in the column
#     df_translated[column] = df[column].astype(str).apply(translate_cell)
#
# # Save the translated DataFrame to a new Excel file
# df_translated.to_excel('translated_excel_file.xlsx', index=False)
#
# print('Translation completed and saved to translated_excel_file.xlsx')
#
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_excel('Datatest.xlsx', sheet_name='Sheet1')

# Convert the 'Series' column to string, filling NaNs with a placeholder
df['Outer wall type'] = df['Outer wall type'].astype(str).replace('nan', 'Unknown')

# Initialize the OneHotEncoder
encoder = OneHotEncoder(sparse=False)

# Fit and transform the 'Series' column
encoded_data = encoder.fit_transform(df[['Outer wall type']])

# Perform hierarchical clustering
linked = linkage(encoded_data, method='ward')

# Plot the dendrogram with truncation
plt.figure(figsize=(10, 7))
dendrogram(linked, orientation='top', truncate_mode='lastp', p=30, distance_sort='descending', show_leaf_counts=True)

# Save the plot
plt.savefig('dendrogram3.png', dpi=300, bbox_inches='tight')

# Show the plot
plt.show()
