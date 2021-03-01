import utils
import pandas as pd
#esta funcion solo la llamamos la primera vez que se ejecuta el programa
#then i would want to evite that this is exectuting every time, it's a one time thing, baby!
def create_reactions_links_to_scrape(path):

    # Leemos el archivo principal y lo pasamos a un df
    datadf=pd.read_csv(path, delimiter= ",", usecols=["link","page_id","post_id"])

    df=pd.DataFrame(datadf)
    print(df)
    print(df['link'])

    df = df.reindex(columns = df.columns.tolist() + ['id','link_id','m_link','post_scraped','comments_scraped','reactions_scraped','shares_scraped','exception'])

    # df.columns = ['id','post_link','link_id','Scraped', 'Me gusta','exception','Me encanta','Me entristece','Me enoja','Me divierte','Me asombra','Me importa','total_count']

    # Añadimos los id al df
    ids = []
    for i in range(len(df)):
        ids.append(i)

    page_id_list = list(df["post_id"])

    post_id_list = list(df["page_id"])


    df["comments_post_link"] = ""
    for i in range(len(page_id_list)):
        df.loc[i,"comments_post_link"] = "https://m.facebook.com/permalink.php?story_fbid=" + str(page_id_list[i])+ "&id=" + str(post_id_list[i])

    print(len(ids))
    df["id"]= ids
    # # Se usan 4 parametros para la función : regex_df_column(el dataframe, texto a buscar, texto a reemplazar, string de la columna)
    df["m_link"] = utils.regex_df_column(df,"https://www.","https://mobile.","link")

    df["post_scraped"] = False
    df["reactions_scraped"] = False
    df["shares_scraped"] = False
    df["comments_scraped"]= False
    
    df
    # Save data of df created and Create File to work with
    df.to_csv("reactions_links_to_scrape.csv",index=False)
    df.to_csv("reactions_links_to_scrape_scraped.csv",index=False)


def create_user_reactions(path):
    #dejar los post ID
    df = pd.DataFrame(columns=['id','user_id','user_link','name','reaction','link_id','exception'])
    df.to_csv("user_reactions_scraped.csv",index=False)

def create_user_comments(path):
    df = pd.DataFrame(columns=['comment_id','message','name','user_id','link_id','comment_type','main_post_link','exception'])
    df.to_csv("user_comments_scraped.csv",index=False)

def create_shares(path):
    df = pd.DataFrame(columns=['user_id','name','user_link','post_id','main_post_link','exception'])
    df.to_csv("shares_scraped.csv",index=False)

