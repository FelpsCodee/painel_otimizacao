class pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        
    def exibir_info(self):
        print(f"nome: {self.nome}, idade: {self.idade}")
        

pessoa1 = pessoa('Felipe',18)
pessoa1.exibir_info()