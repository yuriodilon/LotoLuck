import pandas as pd
from django.core.management.base import BaseCommand
from websiteApp.models import Concurso  # Certifique-se de usar o app correto

class Command(BaseCommand):
    help = "Importar dados de concursos para o banco de dados a partir de uma planilha Excel."

    def handle(self, *args, **kwargs):
        # Caminho do arquivo Excel
        file_path = "lotofacil.xlsx"

        try:
            # Carregar a planilha
            df = pd.read_excel(file_path)

            # Contadores para monitorar o progresso
            adicionados = 0
            ignorados = 0
            erros = 0
            concursos_nao_adicionados = []

            # Iterar sobre as linhas da planilha
            for _, row in df.iterrows():
                try:
                    # Ignorar concursos já existentes
                    if Concurso.objects.filter(nConcurso=row["Concurso"]).exists():
                        self.stdout.write(f"Ignorando concurso {row['Concurso']} (já existe)")
                        ignorados += 1
                        continue

                    # Validar campos obrigatórios
                    nConcurso = row["Concurso"]
                    data_concurso = row["Data Sorteio"]
                    bolas = [row[f"Bola{i}"] for i in range(1, 16)]

                    # Verificar se as bolas estão presentes
                    if any(pd.isna(bola) for bola in bolas):
                        self.stdout.write(
                            self.style.ERROR(
                                f"Concurso {nConcurso} ignorado: faltam números das bolas."
                            )
                        )
                        concursos_nao_adicionados.append(nConcurso)
                        erros += 1
                        continue

                    # Criar o registro no banco de dados com apenas os campos obrigatórios
                    Concurso.objects.create(
                        nConcurso=nConcurso,
                        data_concurso=data_concurso,
                        bola1=row["Bola1"],
                        bola2=row["Bola2"],
                        bola3=row["Bola3"],
                        bola4=row["Bola4"],
                        bola5=row["Bola5"],
                        bola6=row["Bola6"],
                        bola7=row["Bola7"],
                        bola8=row["Bola8"],
                        bola9=row["Bola9"],
                        bola10=row["Bola10"],
                        bola11=row["Bola11"],
                        bola12=row["Bola12"],
                        bola13=row["Bola13"],
                        bola14=row["Bola14"],
                        bola15=row["Bola15"],
                    )

                    # Log de progresso
                    self.stdout.write(f"Criado concurso {nConcurso}")
                    adicionados += 1

                except Exception as e:
                    # Logar erros ao criar o registro, mas continuar o processo
                    self.stdout.write(
                        self.style.ERROR(f"Erro ao criar concurso {row['Concurso']}: {e}")
                    )
                    concursos_nao_adicionados.append(row["Concurso"])
                    erros += 1

            # Mensagem final
            if adicionados > 0 or ignorados > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Processamento concluído! {adicionados} concursos adicionados, {ignorados} ignorados."
                    )
                )
            if erros > 0:
                self.stdout.write(
                    self.style.ERROR(f"Finalizado com {erros} erro(s) ao processar.")
                )
                self.stdout.write(
                    self.style.ERROR(f"Concursos não adicionados: {concursos_nao_adicionados}")
                )
            else:
                self.stdout.write(self.style.SUCCESS("Importação concluída sem erros!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Arquivo '{file_path}' não encontrado."))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Coluna ausente: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro inesperado: {e}"))
