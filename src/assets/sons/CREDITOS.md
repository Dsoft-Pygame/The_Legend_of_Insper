# Créditos dos sons

Todos os sons desta pasta foram **feitos pelo próprio grupo**, gerados por código (síntese de ondas quadrada, triangular, serra, seno e ruído) com o script `ferramentas/gerar_sons.py`. Nenhum arquivo veio de terceiros, então não há licença externa a seguir.

Para gerar de novo (mesmo resultado, a semente é fixa), da raiz do repositório:

```
python ferramentas/gerar_sons.py
```

O script usa só a biblioteca padrão do Python. Para as músicas em `.ogg` ele chama o `ffmpeg`; sem o `ffmpeg`, deixa as músicas em `.wav`.

## Efeitos (`.wav`)

| Arquivo | Som | Origem |
|---|---|---|
| `ataque.wav` | golpe: "fuuu" de ruído descendo com estalo agudo | gerado pelo grupo |
| `acerto.wav` | pancada grave e curta | gerado pelo grupo |
| `inimigo_derrotado.wav` | arpejo descendo e um "puf" | gerado pelo grupo |
| `chefe_derrotado.wav` | explosão longa e fanfarra de vitória | gerado pelo grupo |
| `heroi_derrotado.wav` | notas tristes descendo | gerado pelo grupo |
| `porta.wav` | subida rápida, como teletransporte | gerado pelo grupo |
| `menu_mover.wav` | bip curtinho | gerado pelo grupo |
| `menu_confirmar.wav` | dois bips subindo | gerado pelo grupo |

## Músicas (`.ogg`, tocam em loop)

| Arquivo | Música | Duração do loop | Origem |
|---|---|---|---|
| `musica_menu.ogg` | calma, Lá menor, 90 bpm | 21 s | composta e gerada pelo grupo |
| `musica_torre.ogg` | aventura, Ré menor, 132 bpm | 29 s | composta e gerada pelo grupo |
| `musica_chefe.ogg` | tensa, Mi menor, 156 bpm | 12 s | composta e gerada pelo grupo |
| `musica_resultado.ogg` | tranquila, Dó maior, 100 bpm | 19 s | composta e gerada pelo grupo |

Se alguém trocar um arquivo por um de fora (por exemplo, do opengameart.org com licença CC0), anote aqui o nome, o autor, a licença e o link.
