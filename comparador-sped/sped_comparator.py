"""
Módulo para comparação de arquivos SPED Fiscal.
"""

from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
from sped_parser import SpedParser, SpedRecord


class DifferenceType(Enum):
    """Tipos de diferenças encontradas na comparação."""
    RECORD_ADDED = "Registro adicionado"
    RECORD_REMOVED = "Registro removido"
    RECORD_MODIFIED = "Registro modificado"
    FIELD_CHANGED = "Campo alterado"


@dataclass
class FieldDifference:
    """Representa uma diferença em um campo específico."""
    field_index: int
    field_name: str
    old_value: str
    new_value: str


@dataclass
class RecordDifference:
    """Representa uma diferença entre registros."""
    record_type: str
    difference_type: DifferenceType
    line_number_file1: Optional[int]
    line_number_file2: Optional[int]
    record_file1: Optional[SpedRecord]
    record_file2: Optional[SpedRecord]
    field_differences: List[FieldDifference]
    
    def __str__(self):
        if self.difference_type == DifferenceType.RECORD_ADDED:
            return f"+ Linha {self.line_number_file2}: {self.record_type} adicionado"
        elif self.difference_type == DifferenceType.RECORD_REMOVED:
            return f"- Linha {self.line_number_file1}: {self.record_type} removido"
        elif self.difference_type == DifferenceType.RECORD_MODIFIED:
            return f"~ Linhas {self.line_number_file1}->{self.line_number_file2}: {self.record_type} modificado ({len(self.field_differences)} campos alterados)"
        else:
            return f"? Diferença desconhecida em {self.record_type}"


class SpedComparator:
    """Comparador de arquivos SPED Fiscal."""
    
    def __init__(self, file1_path: str, file2_path: str):
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.parser1 = SpedParser(file1_path)
        self.parser2 = SpedParser(file2_path)
        self.differences: List[RecordDifference] = []
        
    def compare(self) -> List[RecordDifference]:
        """Executa a comparação completa entre os arquivos."""
        print("Fazendo parsing dos arquivos...")
        self.parser1.parse_file()
        self.parser2.parse_file()
        
        print(f"Arquivo 1: {self.parser1.get_total_records()} registros")
        print(f"Arquivo 2: {self.parser2.get_total_records()} registros")
        
        # Comparar registros
        self._compare_records()
        
        return self.differences
    
    def _compare_records(self) -> None:
        """Compara registros entre os dois arquivos."""
        # Obter todos os tipos de registros únicos
        types1 = set(self.parser1.get_record_types())
        types2 = set(self.parser2.get_record_types())
        all_types = types1.union(types2)
        
        for record_type in sorted(all_types):
            self._compare_records_by_type(record_type)
    
    def _compare_records_by_type(self, record_type: str) -> None:
        """Compara registros de um tipo específico."""
        records1 = self.parser1.get_records_by_type(record_type)
        records2 = self.parser2.get_records_by_type(record_type)
        
        # Criar mapeamentos para comparação mais eficiente
        map1 = self._create_record_map(records1)
        map2 = self._create_record_map(records2)
        
        # Encontrar registros removidos
        for key in map1:
            if key not in map2:
                record = map1[key]
                self.differences.append(RecordDifference(
                    record_type=record_type,
                    difference_type=DifferenceType.RECORD_REMOVED,
                    line_number_file1=record.line_number,
                    line_number_file2=None,
                    record_file1=record,
                    record_file2=None,
                    field_differences=[]
                ))
        
        # Encontrar registros adicionados
        for key in map2:
            if key not in map1:
                record = map2[key]
                self.differences.append(RecordDifference(
                    record_type=record_type,
                    difference_type=DifferenceType.RECORD_ADDED,
                    line_number_file1=None,
                    line_number_file2=record.line_number,
                    record_file1=None,
                    record_file2=record,
                    field_differences=[]
                ))
        
        # Comparar registros que existem em ambos
        for key in map1:
            if key in map2:
                record1 = map1[key]
                record2 = map2[key]
                field_diffs = self._compare_record_fields(record1, record2)
                
                if field_diffs:
                    self.differences.append(RecordDifference(
                        record_type=record_type,
                        difference_type=DifferenceType.RECORD_MODIFIED,
                        line_number_file1=record1.line_number,
                        line_number_file2=record2.line_number,
                        record_file1=record1,
                        record_file2=record2,
                        field_differences=field_diffs
                    ))
    
    def _create_record_map(self, records: List[SpedRecord]) -> Dict[str, SpedRecord]:
        """Cria um mapeamento de registros baseado em uma chave única."""
        record_map = {}
        
        for i, record in enumerate(records):
            # Para registros com múltiplas ocorrências, usar índice na chave
            key = f"{record.get_key()}_{i}"
            record_map[key] = record
            
        return record_map
    
    def _compare_record_fields(self, record1: SpedRecord, record2: SpedRecord) -> List[FieldDifference]:
        """Compara os campos entre dois registros."""
        differences = []
        
        # Comparar número de campos
        max_fields = max(len(record1.fields), len(record2.fields))
        
        for i in range(max_fields):
            value1 = record1.fields[i] if i < len(record1.fields) else ""
            value2 = record2.fields[i] if i < len(record2.fields) else ""
            
            if value1 != value2:
                differences.append(FieldDifference(
                    field_index=i,
                    field_name=f"Campo_{i}",
                    old_value=value1,
                    new_value=value2
                ))
        
        return differences
    
    def get_summary(self) -> Dict[str, int]:
        """Retorna um resumo das diferenças encontradas."""
        summary = {
            "total_differences": len(self.differences),
            "records_added": 0,
            "records_removed": 0,
            "records_modified": 0
        }
        
        for diff in self.differences:
            if diff.difference_type == DifferenceType.RECORD_ADDED:
                summary["records_added"] += 1
            elif diff.difference_type == DifferenceType.RECORD_REMOVED:
                summary["records_removed"] += 1
            elif diff.difference_type == DifferenceType.RECORD_MODIFIED:
                summary["records_modified"] += 1
        
        return summary
    
    def get_differences_by_type(self, record_type: str) -> List[RecordDifference]:
        """Retorna diferenças filtradas por tipo de registro."""
        return [diff for diff in self.differences if diff.record_type == record_type]