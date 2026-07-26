"""
Utilities untuk extract kolom dari django-tables2 Table
sehingga Excel export bisa sesuai dengan kolom yang ditampilkan
"""
from django_tables2 import Column


def get_table_columns(table_class):
    """
    Extract kolom dari django-tables2 table class
    
    Usage:
        from config.utils.table_columns import get_table_columns
        from umum.tables import PegawaiTable
        
        columns = get_table_columns(PegawaiTable)
        # Result: [('nip', 'NIP'), ('nama', 'Nama Pegawai'), ...]
    
    Args:
        table_class: Django-tables2 Table class
    
    Returns:
        List of tuples: [(field_name, column_header), ...]
    """
    columns = []
    
    for name, column in table_class.base_columns.items():
        if isinstance(column, Column):
            # Get verbose_name dari column, atau use name
            header = column.verbose_name or name.replace('_', ' ').title()
            columns.append((name, header))
    
    return columns


def get_table_columns_from_instance(table_instance):
    """
    Extract kolom dari django-tables2 table instance
    
    Args:
        table_instance: Django-tables2 Table instance
    
    Returns:
        List of tuples: [(field_name, column_header), ...]
    """
    return get_table_columns(table_instance.__class__)
