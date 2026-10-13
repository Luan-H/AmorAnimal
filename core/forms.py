from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite seu usuário',
            'required': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite sua senha',
            'required': True
        })
    )

class AnimalForm(forms.Form):
    STATUS_CHOICES = [
        ('Disponível', 'Disponível para Adoção'),
        ('Em Tratamento', 'Em Tratamento / Recuperação'),
        ('Adotado', 'Adotado (Final Feliz)'),
    ]

    nome = forms.CharField(
        label='Nome do Animal',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Negão, Vitória, Pretinha...',
            'required': True
        })
    )
    historia = forms.CharField(
        label='História / Descrição do Resgate',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Conte um pouco sobre como ele foi resgatado e a evolução dele...'
        })
    )
    status_adocao = forms.ChoiceField(
        label='Status Atual',
        choices=STATUS_CHOICES,
        initial='Disponível',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    foto_antes = forms.ImageField(
        label='Foto do Antes (Resgate)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    foto_depois = forms.ImageField(
        label='Foto do Depois (Transformação)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

class PatrocinadorForm(forms.Form):
    nome = forms.CharField(
        label='Nome da Empresa / Parceiro',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: MedPort, PetMarket...',
            'required': True
        })
    )
    link_externo = forms.URLField(
        label='Link do Instagram ou Site',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.instagram.com/empresa'
        })
    )
    logotipo = forms.ImageField(
        label='Logotipo da Empresa',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    ativo = forms.BooleanField(
        label='Exibir no site?',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ConfiguracaoForm(forms.Form):
    hero_titulo = forms.CharField(
        label='Título Principal (Hero)',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    hero_subtitulo = forms.CharField(
        label='Frase de Impacto (Subtítulo)',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    sobre_titulo = forms.CharField(
        label='Título da Seção Sobre',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    sobre_texto_1 = forms.CharField(
        label='Texto Sobre (Primeiro Parágrafo)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True})
    )
    sobre_texto_2 = forms.CharField(
        label='Texto Sobre (Segundo Parágrafo)',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True})
    )
    chave_pix = forms.CharField(
        label='Chave PIX para Doações',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    instagram_usuario = forms.CharField(
        label='Nome do Usuário no Instagram (Ex: @amoranimal.cuiaba)',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    instagram_link = forms.URLField(
        label='Link Completo do Instagram',
        widget=forms.URLInput(attrs={'class': 'form-control', 'required': True})
    )
    whatsapp_numero = forms.CharField(
        label='Número do WhatsApp exibido (Ex: (65) 9 8119-3351)',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    whatsapp_link = forms.URLField(
        label='Link direto da conversa no WhatsApp (wa.me)',
        widget=forms.URLInput(attrs={'class': 'form-control', 'required': True})
    )

class SolicitacaoAdocaoForm(forms.Form):
    animal_id = forms.CharField(widget=forms.HiddenInput())
    animal_nome = forms.CharField(widget=forms.HiddenInput())
    nome_interessado = forms.CharField(
        label='Seu Nome Completo',
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo',
            'required': True
        })
    )
    telefone = forms.CharField(
        label='Seu WhatsApp (com DDD)',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: (65) 99999-9999',
            'required': True
        })
    )
    mensagem = forms.CharField(
        label='Mensagem ou motivo do interesse (opcional)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Conte se já tem outros animais, onde mora...'
        })
    )

