# Assistant de Francais

Assistant de français is a Discord bot. It provides a /definir
command, which provides a definition to the given term.

Example interaction:

```
User: /definir essor

Bot: essor (m.) : Progrès rapide et remarquable d'une activité, d'un mouvement, d'une situation ; développement, expansion.
Exemple : L'essor économique du pays s'est traduit par une augmentation significative de la production industrielle.
```


## Feature Requests

Feature requests are welcome. Please submit feature requests in the form of a Github issue.

## Developing

You will neeed to sign up to sign up to the [Discover Developer Portal](https://discord.com/developers/) and create a bot.

You will also need to create an API key from [OpenRouter](https://openrouter.ai/).

Then, set the necessary environment variables. You can copy the file `.env.default` to `.env` and override the variables as needed.

Finally, start the bot with `docker-compose up`.

## Hosting

Please follow the same instructions as Developing