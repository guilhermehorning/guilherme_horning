"""
Módulo para geração de relatórios de comparação SPED.
"""

from typing import List, Dict
from datetime import datetime
from pathlib import Path
from sped_comparator import SpedComparator, RecordDifference, DifferenceType, FieldDifference


class SpedReportGenerator:
    """Gerador de relatórios para comparação de arquivos SPED."""
    
    def __init__(self, comparator: SpedComparator):
        self.comparator = comparator
        
    def generate_console_report(self) -> None:
        """Gera relatório no console."""
        print("\n" + "="*80)
        print("RELATÓRIO DE COMPARAÇÃO SPED FISCAL")
        print("="*80)
        
        print(f"\nArquivo 1: {Path(self.comparator.file1_path).name}")
        print(f"Arquivo 2: {Path(self.comparator.file2_path).name}")
        print(f"Data da comparação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Resumo geral
        summary = self.comparator.get_summary()
        print(f"\n--- RESUMO GERAL ---")
        print(f"Total de diferenças encontradas: {summary['total_differences']}")
        print(f"Registros adicionados: {summary['records_added']}")
        print(f"Registros removidos: {summary['records_removed']}")
        print(f"Registros modificados: {summary['records_modified']}")
        
        if summary['total_differences'] == 0:
            print("\n✅ Os arquivos são idênticos!")
            return
        
        # Estatísticas por tipo de registro
        self._print_statistics_by_record_type()
        
        # Detalhes das diferenças
        print(f"\n--- DETALHES DAS DIFERENÇAS ---")
        self._print_detailed_differences()
        
        print("\n" + "="*80)
    
    def _print_statistics_by_record_type(self) -> None:
        """Imprime estatísticas por tipo de registro."""
        print(f"\n--- ESTATÍSTICAS POR TIPO DE REGISTRO ---")
        
        # Agrupar diferenças por tipo de registro
        diff_by_type = {}
        for diff in self.comparator.differences:
            record_type = diff.record_type
            if record_type not in diff_by_type:
                diff_by_type[record_type] = {
                    'added': 0,
                    'removed': 0,
                    'modified': 0,
                    'total': 0
                }
            
            diff_by_type[record_type]['total'] += 1
            
            if diff.difference_type == DifferenceType.RECORD_ADDED:
                diff_by_type[record_type]['added'] += 1
            elif diff.difference_type == DifferenceType.RECORD_REMOVED:
                diff_by_type[record_type]['removed'] += 1
            elif diff.difference_type == DifferenceType.RECORD_MODIFIED:
                diff_by_type[record_type]['modified'] += 1
        
        # Imprimir tabela
        print(f"{'Tipo':^8} | {'Total':^6} | {'Adicionados':^11} | {'Removidos':^9} | {'Modificados':^11}")
        print("-" * 60)
        
        for record_type in sorted(diff_by_type.keys()):
            stats = diff_by_type[record_type]
            print(f"{record_type:^8} | {stats['total']:^6} | {stats['added']:^11} | {stats['removed']:^9} | {stats['modified']:^11}")
    
    def _print_detailed_differences(self) -> None:
        """Imprime detalhes das diferenças encontradas."""
        current_type = None
        
        for diff in sorted(self.comparator.differences, key=lambda x: (x.record_type, x.line_number_file1 or x.line_number_file2 or 0)):
            # Cabeçalho por tipo de registro
            if diff.record_type != current_type:
                current_type = diff.record_type
                print(f"\n📋 REGISTRO {current_type}:")
                print("-" * 50)
            
            # Imprimir diferença
            if diff.difference_type == DifferenceType.RECORD_ADDED:
                print(f"  ➕ ADICIONADO (Linha {diff.line_number_file2}):")
                print(f"     {diff.record_file2.raw_line}")
                
            elif diff.difference_type == DifferenceType.RECORD_REMOVED:
                print(f"  ➖ REMOVIDO (Linha {diff.line_number_file1}):")
                print(f"     {diff.record_file1.raw_line}")
                
            elif diff.difference_type == DifferenceType.RECORD_MODIFIED:
                print(f"  🔄 MODIFICADO (Linha {diff.line_number_file1} -> {diff.line_number_file2}):")
                print(f"     Arquivo 1: {diff.record_file1.raw_line}")
                print(f"     Arquivo 2: {diff.record_file2.raw_line}")
                
                # Mostrar campos alterados
                if diff.field_differences:
                    print("     Campos alterados:")
                    for field_diff in diff.field_differences:
                        print(f"       • Campo {field_diff.field_index}: '{field_diff.old_value}' -> '{field_diff.new_value}'")
            
            print()
    
    def generate_html_report(self, output_file: str) -> None:
        """Gera relatório em HTML."""
        html_content = self._generate_html_content()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Relatório HTML gerado: {output_file}")
    
    def _generate_html_content(self) -> str:
        """Gera o conteúdo HTML do relatório."""
        summary = self.comparator.get_summary()
        
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Comparação SPED Fiscal</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f8ff; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .difference {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .added {{ border-left-color: #4CAF50; background-color: #f1f8e9; }}
        .removed {{ border-left-color: #f44336; background-color: #ffebee; }}
        .modified {{ border-left-color: #ff9800; background-color: #fff3e0; }}
        .record-type {{ font-weight: bold; color: #1976d2; margin-top: 20px; }}
        .field-changes {{ margin-left: 20px; font-size: 0.9em; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
        th {{ background-color: #f2f2f2; }}
        .code {{ font-family: monospace; background-color: #f5f5f5; padding: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Comparação SPED Fiscal</h1>
        <p><strong>Arquivo 1:</strong> {Path(self.comparator.file1_path).name}</p>
        <p><strong>Arquivo 2:</strong> {Path(self.comparator.file2_path).name}</p>
        <p><strong>Data da comparação:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Resumo Geral</h2>
        <p><strong>Total de diferenças:</strong> {summary['total_differences']}</p>
        <p><strong>Registros adicionados:</strong> {summary['records_added']}</p>
        <p><strong>Registros removidos:</strong> {summary['records_removed']}</p>
        <p><strong>Registros modificados:</strong> {summary['records_modified']}</p>
    </div>
        """
        
        if summary['total_differences'] == 0:
            html += "<div class='summary'><h2>✅ Os arquivos são idênticos!</h2></div>"
        else:
            html += self._generate_html_details()
        
        html += """
</body>
</html>
        """
        
        return html
    
    def _generate_html_details(self) -> str:
        """Gera os detalhes em HTML."""
        html = "<h2>Detalhes das Diferenças</h2>\n"
        
        current_type = None
        
        for diff in sorted(self.comparator.differences, key=lambda x: (x.record_type, x.line_number_file1 or x.line_number_file2 or 0)):
            if diff.record_type != current_type:
                current_type = diff.record_type
                html += f"<div class='record-type'>📋 REGISTRO {current_type}</div>\n"
            
            css_class = ""
            icon = ""
            
            if diff.difference_type == DifferenceType.RECORD_ADDED:
                css_class = "added"
                icon = "➕"
                title = f"ADICIONADO (Linha {diff.line_number_file2})"
                content = f"<div class='code'>{diff.record_file2.raw_line}</div>"
                
            elif diff.difference_type == DifferenceType.RECORD_REMOVED:
                css_class = "removed"
                icon = "➖"
                title = f"REMOVIDO (Linha {diff.line_number_file1})"
                content = f"<div class='code'>{diff.record_file1.raw_line}</div>"
                
            elif diff.difference_type == DifferenceType.RECORD_MODIFIED:
                css_class = "modified"
                icon = "🔄"
                title = f"MODIFICADO (Linha {diff.line_number_file1} -> {diff.line_number_file2})"
                content = f"""
                <div class='code'>Arquivo 1: {diff.record_file1.raw_line}</div>
                <div class='code'>Arquivo 2: {diff.record_file2.raw_line}</div>
                """
                
                if diff.field_differences:
                    content += "<div class='field-changes'><strong>Campos alterados:</strong><ul>"
                    for field_diff in diff.field_differences:
                        content += f"<li>Campo {field_diff.field_index}: '{field_diff.old_value}' -> '{field_diff.new_value}'</li>"
                    content += "</ul></div>"
            
            html += f"""
            <div class="difference {css_class}">
                <strong>{icon} {title}</strong>
                {content}
            </div>
            """
        
        return html