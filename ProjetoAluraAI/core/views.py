from django.views.generic.edit import FormView
from .forms import Cidade
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from django.shortcuts import render

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY') # Por aqui não ta dando certo
client = genai.Client(api_key=GOOGLE_API_KEY)
modelo = "models/gemini-2.0-flash"

# Aqui que a mágica acontece:
def guia_turistico_t1000(cidade_atual):
    gem = f'''
    Você é um guia turístico virtual chamado T1000, especializado em fornecer
    informações detalhadas e atualizadas sobre diversas cidades. Seu objetivo é
    auxiliar os usuários a descobrirem o melhor que cada local tem a oferecer,
    de forma amigável, concisa e objetiva. Inclua emojis relevantes para tornar
    a apresentação mais atrativa.

    Para a cidade de {cidade_atual}, forneça as seguintes informações,
    obtidas através de pesquisa na web, use o google para pegar as informações reais e precisas:
    '''
    msg = f'''
    1. Hoteis Mais Bem Avaliadosde de {cidade_atual}:

    * Apresente os 5 hoteis mais bem avaliados da cidade, com base em
        avaliações do Google.
    * Para cada hotel, inclua:
        * Nome do hotel.
        * Se tem piscina ou não
        * Um emoji representativo.
    
    2. Restaurantes Mais Bem Avaliados de {cidade_atual}:

    * Apresente os 5 restaurantes mais bem avaliados da cidade, com base em
        avaliações do Google.
    * Para cada restaurante, inclua:
        * Nome do restaurante.
        * Uma breve descrição do tipo de culinária ou ambiente do restaurante.
        * Um emoji representativo (ex: 🍕 para pizza, 🍣 para japonês, 🍔 para hambúrguer).

    3. Principais Pontos Turísticos de {cidade_atual}:

    * Liste os 5 pontos turísticos mais visitados e considerados imperdíveis
        na cidade.
    * Para cada ponto turístico, inclua:
        * Nome do ponto turístico.
        * Uma breve descrição de sua importância ou atrativo.
        * Um emoji representativo (ex: 🌳 para parque, 🏛️ para museu, ⛪ para igreja).

    4. Previsão do Tempo para a Semana de {cidade_atual}:

    * Forneça a previsão do tempo para os próximos 7 dias na cidade.
    * Inclua:
        * Dia da semana.
        * Condição geral do tempo (ex: ensolarado, nublado, chuvoso).
        * Temperatura máxima e mínima previstas.
        * Probabilidade de chuva (%).
        * Um emoji representativo para cada dia (ex: ☀️ para ensolarado, 🌧️ para chuvoso).

    Estruture sua resposta de forma clara e organizada, utilizando títulos e
    subtítulos quando apropriado.
    '''
    chat_config = types.GenerateContentConfig(
        system_instruction=gem
    )
    chat = client.chats.create(model=modelo, config=chat_config)

    response = chat.send_message(msg)
    return response.text


class GuiaT1000(FormView):
    template_name = 'index.html'  # Caminho para seu template
    form_class = Cidade
    success_url = reverse_lazy('index')  # URL para redirecionar após o sucesso

    def form_valid(self, form):
        city = form.cleaned_data['city']
        response_data = guia_turistico_t1000(city)
        # print(response_data)
        # Renderiza o template 'index.html' novamente,
        # passando os dados da resposta no contexto
        return render(self.request, self.template_name, {'form': form, 'response': response_data})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Garante que o formulário seja sempre passado para o template
        context['form'] = self.form_class()
        return context
