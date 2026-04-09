from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def exportar_planilha(numero_pedido, nome_cliente, itens):
    pasta_downloads = Path.home() / "Downloads"
    nome_arquivo = pasta_downloads / f"{nome_cliente}.pdf"

    pdf = canvas.Canvas(str(nome_arquivo), pagesize=A4)
    largura, altura = A4

    y = altura - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Pedido do Cliente")
    y -= 30

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Número do pedido: {numero_pedido}")
    y -= 20
    pdf.drawString(50, y, f"Cliente: {nome_cliente}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "Código")
    pdf.drawString(120, y, "Item")
    pdf.drawString(280, y, "Qtd")
    pdf.drawString(330, y, "Valor Unit.")
    pdf.drawString(450, y, "Total")
    y -= 20

    pdf.setFont("Helvetica", 10)
    total_geral = 0

    for item in itens:
        total_item = item["total"]
        total_geral += total_item

        # quebra de página
        if y < 60:
            pdf.showPage()
            y = altura - 50

            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(50, y, "Código")
            pdf.drawString(120, y, "Item")
            pdf.drawString(280, y, "Qtd")
            pdf.drawString(330, y, "Valor Unit.")
            pdf.drawString(450, y, "Total")
            y -= 20

            pdf.setFont("Helvetica", 10)

        pdf.drawString(50, y, str(item["codigo"]))
        pdf.drawString(120, y, str(item["item"]))
        pdf.drawString(280, y, str(item["quantidade"]))
        pdf.drawString(330, y, formatar_moeda(item["valor_unitario"]))
        pdf.drawString(450, y, formatar_moeda(total_item))
        y -= 18

    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(330, y, "Total geral:")
    pdf.drawString(450, y, formatar_moeda(total_geral))

    pdf.save()
    return str(nome_arquivo)