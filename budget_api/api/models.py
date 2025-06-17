from django.db import models
import hashlib

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.categoria.nome} - {self.nome}"

    class Meta:
        ordering = ['categoria__nome', 'nome']
        unique_together = ('categoria', 'nome')
        verbose_name = "Subcategoria"
        verbose_name_plural = "Subcategorias"

class Origem(models.Model):
    nome = models.CharField(max_length=100, unique=True) # e.g., Bank Name, Credit Card Name
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = "Origem"
        verbose_name_plural = "Origens"

class Lancamento(models.Model):
    STATUS_CONCILIACAO_CHOICES = [
        ('pendente', 'Pendente de Conciliação'),
        ('conciliado', 'Conciliado'),
        ('ignorado', 'Ignorado'),
    ]

    TIPO_LANCAMENTO_CHOICES = [
        ('DEBIT', 'Débito'),
        ('CREDIT', 'Crédito'),
        ('OTHER', 'Outro'),
    ]

    data_transacao = models.DateField(help_text="Data da transação")
    data_upload = models.DateTimeField(auto_now_add=True, help_text="Data do upload do OFX/criação do registro")
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor da transação")
    descricao_original = models.CharField(max_length=255, help_text="Descrição original do OFX ou entrada manual")
    tipo_transacao = models.CharField(max_length=10, choices=TIPO_LANCAMENTO_CHOICES, help_text="Tipo de transação (Débito/Crédito)")

    status_conciliacao = models.CharField(
        max_length=10,
        choices=STATUS_CONCILIACAO_CHOICES,
        default='pendente',
        help_text="Status da conciliação do lançamento"
    )
    referencia_mes = models.CharField(max_length=7, blank=True, null=True, help_text="Mês de referência (AAAA-MM)") # e.g., 2023-10

    # Campos editáveis na conciliação
    descricao_editada = models.CharField(max_length=255, blank=True, null=True, help_text="Descrição editada pelo usuário")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    sub_categoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True, blank=True)
    origem = models.ForeignKey(Origem, on_delete=models.SET_NULL, null=True, blank=True, help_text="Origem do lançamento (Banco, Cartão)")

    hash_transacao = models.CharField(max_length=64, unique=True, blank=True, null=True, editable=False, help_text="Hash para identificar transações duplicadas")

    def save(self, *args, **kwargs):
        if not self.hash_transacao and self.descricao_original: # Ensure there's a description to hash
            # Create a hash based on key fields to help identify duplicates from OFX
            unique_string = f"{self.data_transacao}-{self.valor}-{self.descricao_original}-{self.tipo_transacao}"
            self.hash_transacao = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.data_transacao} - {self.get_descricao_display()} - {self.valor}"

    def get_descricao_display(self):
        return self.descricao_editada if self.descricao_editada else self.descricao_original

    class Meta:
        ordering = ['-data_transacao', '-data_upload']
        verbose_name = "Lançamento"
        verbose_name_plural = "Lançamentos"
