"""
Módulo para parsing e análise de arquivos SPED Fiscal.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SpedRecord:
    """Representa um registro SPED com seus campos."""
    line_number: int
    record_type: str
    fields: List[str]
    raw_line: str
    
    def __str__(self):
        return f"Linha {self.line_number}: {self.record_type} - {len(self.fields)} campos"
    
    def get_key(self) -> str:
        """Gera uma chave única para o registro baseada no tipo e campos principais."""
        # Para registros com múltiplas ocorrências, incluir mais campos na chave
        key_fields = [self.record_type]
        
        # Adicionar campos específicos baseados no tipo de registro
        if len(self.fields) > 1:
            key_fields.extend(self.fields[:3])  # Primeiros 3 campos para diferenciação
            
        return "|".join(key_fields)


class SpedParser:
    """Parser para arquivos SPED Fiscal."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.records: List[SpedRecord] = []
        self.records_by_type: Dict[str, List[SpedRecord]] = {}
        
    def parse_file(self) -> None:
        """Faz o parsing completo do arquivo SPED."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")
            
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if line:
                    record = self._parse_line(line, line_number)
                    if record:
                        self.records.append(record)
                        
                        # Organizar por tipo de registro
                        if record.record_type not in self.records_by_type:
                            self.records_by_type[record.record_type] = []
                        self.records_by_type[record.record_type].append(record)
    
    def _parse_line(self, line: str, line_number: int) -> Optional[SpedRecord]:
        """Faz o parsing de uma linha do arquivo SPED."""
        # Padrão SPED: |campo1|campo2|campo3|...|
        if not line.startswith('|') or not line.endswith('|'):
            return None
            
        # Remove os pipes do início e fim e divide pelos pipes internos
        line_content = line[1:-1]  # Remove | do início e fim
        fields = line_content.split('|')
        
        if not fields:
            return None
            
        record_type = fields[0] if fields else ""
        
        return SpedRecord(
            line_number=line_number,
            record_type=record_type,
            fields=fields,
            raw_line=line
        )
    
    def get_records_by_type(self, record_type: str) -> List[SpedRecord]:
        """Retorna todos os registros de um tipo específico."""
        return self.records_by_type.get(record_type, [])
    
    def get_record_types(self) -> List[str]:
        """Retorna todos os tipos de registros encontrados no arquivo."""
        return sorted(self.records_by_type.keys())
    
    def get_total_records(self) -> int:
        """Retorna o total de registros no arquivo."""
        return len(self.records)
    
    def get_statistics(self) -> Dict[str, int]:
        """Retorna estatísticas dos registros por tipo."""
        return {
            record_type: len(records) 
            for record_type, records in self.records_by_type.items()
        }