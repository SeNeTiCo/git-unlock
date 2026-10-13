# Git Unlock

Um programa que nasce **bloqueado**. Ele só é liberado quando o repositório estiver no estado correto, e quem decide isso é o Git, não o Python.

Seu trabalho: investigar o repositório, fazer as operações certas e deixar tudo registrado no histórico.

## Requisitos

- Python 3.8+
- Git 2.28+
- `user.name` e `user.email` configurados no Git

## Como começar

```bash
git clone <URL-DO-REPOSITORIO>
cd git-unlock
python main.py
```

O programa vai dizer que está bloqueado. Ele não vai dizer o motivo. Descobrir é parte do teste.

## Missão

Deixe o repositório assim:

1. **Branch certa integrada na `main`.** Existe mais de uma branch no repositório, e só uma delas contém trabalho pronto para entrar. As outras não devem entrar na `main`, nem por acidente.
2. **Histórico preservado.** Os commits da branch escolhida precisam continuar visíveis no `git log` da `main`. Não faça squash.
3. **Conflitos resolvidos.** Ao integrar, o `app/config.json` vai conflitar. Resolva assim:
   - `version` final: `1.0.0`
   - `activated`: `true`
   - `modules`: mantenha todos os módulos que existem nas duas pontas
4. **Commit de release.** Depois da integração, faça um commit que preencha o campo `release` do `app/config.json` com `v1.0.0`. A mensagem deve começar com `release:`. Esse precisa ser o **último commit** da `main`.
5. **Tag de lançamento.** Crie a tag **anotada** `v1.0.0` apontando para esse último commit. A mensagem da tag deve explicar, em uma ou duas frases, o que você integrou e por que escolheu essa branch.
6. **Estado final limpo.** Você deve estar na `main`, sem alterações pendentes e sem marcadores de conflito em nenhum arquivo.

Rode `python main.py` quando achar que terminou.

## Pistas de investigação

Você não precisa de nenhum comando exótico. Estes bastam:

```bash
git status
git branch -a
git log --oneline --graph --all
git log <branch> --oneline
git show <commit>
git diff main..<branch>
git tag -n
```

Perguntas que valem a pena se fazer:

- Quais branches existem e o que cada uma tem de diferente?
- O que as mensagens de commit sugerem sobre o estado de cada branch?
- Quais arquivos cada branch altera? Algum deles parece perigoso para a `main`?
- A `main` andou desde que as branches foram criadas?
- Quais tags já existem e a que commits apontam?

## Testes

```bash
python -m unittest discover -s tests
```

Os testes cobrem a validação. Eles não resolvem o desafio por você.

## O que será avaliado

- Investigação do histórico antes de agir
- Escolha da branch correta e justificativa
- Integração com resolução consciente de conflito
- Commits e tag corretos
- Capacidade de explicar suas decisões na conversa

## Aviso

Esta versão valida localmente. Como os arquivos estão com você, nada impede que o validador seja alterado. Isso é esperado: o objetivo aqui é avaliar seu conhecimento de Git, não sua capacidade de burlar o teste. Se você alterar o validador, a conversa seguinte vai ser bem curta.
