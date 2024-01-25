# Hand Tracking Control

## Descrição
Hand Tracking Control é um projeto que permite o controle de diversas funcionalidades do computador através do rastreamento de mãos, utilizando uma webcam. Implementado com as tecnologias de visão computacional OpenCV e MediaPipe, este projeto detecta as mãos e seus movimentos, permitindo controlar o cursor do mouse, clicar, e até mesmo realizar rolagens de tela de maneira intuitiva e interativa.

## Funcionalidades
- Rastreamento em tempo real das mãos usando a webcam.
- Controle do cursor do mouse através dos movimentos das mãos.
- Possibilidade de realizar cliques e rolagens com gestos específicos.
- Interface redimensionável para melhor visualização e interação.

## Gestos Específicos
- **Mão Aberta**: Controla o cursor com o dedo indicador.
- **Polegar Dobrado**: Realiza um clique com o mouse.
- **Dedo Médio e Indicador Levantados**: Rola a tela para cima.
- **Apenas o Indicador Levantado**: Rola a tela para baixo.

## Como Usar
1. Clone o repositório para sua máquina local.
2. Certifique-se de ter todas as dependências instaladas (listadas em `requirements.txt`).
3. Execute o script principal para iniciar o programa.
4. Siga as instruções na tela para interagir com o sistema usando os gestos.

## Dependências
- OpenCV
- MediaPipe
- PyAutoGUI

## Autor
Igor Macedo ([https://github.com/IgorMacedo4])
