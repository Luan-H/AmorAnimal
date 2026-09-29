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
