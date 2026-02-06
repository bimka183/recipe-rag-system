import pandas as pd

def mapping_column(df):
    df.rename(columns={'name': 'title'}, inplace=True)
    df.rename(columns={'ingredients_quantity': 'ingredients'}, inplace=True)
    df.rename(columns={'instructions': 'content'}, inplace=True)
    df.rename(columns={'description': 'description'}, inplace=True)

    df['cook_time_clean'] = pd.to_numeric(df['cook_time (in mins)'], errors='coerce').fillna(0).astype(int)
    df['meta_info'] = df['cook_time_clean'].apply(lambda x: {"cooking_time": x})
    df.dropna(subset=['title'], inplace=True)

    if 'description' not in df.columns:
        df['description'] = df['title']
    else:
        df['description'] = df['description'].fillna(df['title'])

    df['ingredients'] = df['ingredients'].fillna("")
    df['content'] = df['content'].fillna("")
    df['combined_text'] = df['title'] + " " + df['description'] + " " + df['ingredients'] + " " + df['content']
    return df