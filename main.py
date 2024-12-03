import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class AnalizadorPeliculas:
    def __init__(self, ruta_movies, ruta_ratings):
        self.movies = pd.read_csv(ruta_movies)
        self.ratings = pd.read_csv(ruta_ratings)
        self.preparar_datos()

    def preparar_datos(self):
        # Fusionar los datasets
        self.peliculas_con_ratings = self.movies.merge(
            self.ratings.groupby('movieId')['rating'].agg(['mean', 'count']), 
            on='movieId'
        )

    def top_peliculas(self, n=10):
        # Top películas por rating promedio (mínimo de 100 ratings)
        top = self.peliculas_con_ratings[
            self.peliculas_con_ratings['count'] >= 100
        ].sort_values('mean', ascending=False).head(n)
        
        plt.figure(figsize=(12, 6))
        plt.bar(top['title'], top['mean'])
        plt.title(f'Top {n} Películas por Rating Promedio')
        plt.xlabel('Película')
        plt.ylabel('Rating Promedio')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def distribucion_generos(self):
        # Descomponer géneros
        self.peliculas_con_ratings['genres_list'] = self.peliculas_con_ratings['genres'].str.split('|')
        generos_planos = [gen for sublist in self.peliculas_con_ratings['genres_list'] for gen in sublist]
        
        conteo_generos = pd.Series(generos_planos).value_counts()
        
        plt.figure(figsize=(12, 6))
        conteo_generos.plot(kind='bar')
        plt.title('Distribución de Géneros')
        plt.xlabel('Género')
        plt.ylabel('Número de Películas')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def ratings_por_genero(self):
        # Ratings promedio por género
        def extraer_generos(row):
            return row['genres'].split('|')
        
        generos_expandidos = self.peliculas_con_ratings.apply(extraer_generos, axis=1)
        generos_ratings = []

        for index, generos in generos_expandidos.items():
            rating = self.peliculas_con_ratings.loc[index, 'mean']
            for genero in generos:
                generos_ratings.append({'genero': genero, 'rating': rating})
        
        df_generos_ratings = pd.DataFrame(generos_ratings)
        ratings_por_genero = df_generos_ratings.groupby('genero')['rating'].mean().sort_values(ascending=False)
        
        plt.figure(figsize=(12, 6))
        ratings_por_genero.plot(kind='bar')
        plt.title('Rating Promedio por Género')
        plt.xlabel('Género')
        plt.ylabel('Rating Promedio')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

def main():
    ruta_movies = 'data/movies.csv'
    ruta_ratings = 'data/ratings.csv'
    
    analizador = AnalizadorPeliculas(ruta_movies, ruta_ratings)
    
    analizador.top_peliculas()
    analizador.distribucion_generos()
    analizador.ratings_por_genero()

if __name__ == "__main__":
    main()