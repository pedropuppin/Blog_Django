- o site_setup foi criado para fazer as configurações do site

- cria na área administrativa do django uma parte onde o user possa cofigurar o site

- no models.py criamos o modelo e precisamos registrar ele no admin.py pra ele aparecer na tela

- criamos o context_processor.py e registramos ele nos TEMPLATES
    . é uma forma de possibilitar um contexto global. Conseguimos chamar o exemple lá no index, mesmo sem ter passado um contexto na view que chama a página.
    
    . é util para cassos onde vc precisa de alguma coisa disponível em muitos templates de diferentes apps da sua aplicação.
    
    . tem que ser usado com cuidado pois toda vez que vc acessar uma página do seu app ele vai fazer uma query pra puxar os dados, isso pode causar lentidão.