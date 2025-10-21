import { Injectable, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../../common/prisma/prisma.service';
import { Form, FormField, FieldType } from '@prisma/client';

@Injectable()
export class SchemaService {
  constructor(private prisma: PrismaService) {}

  async generateTableSchema(form: Form, fields: FormField[]) {
    const tableName = `form_${form.key}_v${form.currentVersion}`;
    
    // Generate DDL for the table
    const ddl = this.buildCreateTableDDL(tableName, fields);
    
    // Record in schema registry
    await this.prisma.schemaRegistry.create({
      data: {
        formId: form.id,
        version: form.currentVersion,
        tableName,
        ddl,
      },
    });

    // Update table alias
    await this.prisma.tableAlias.upsert({
      where: { formId: form.id },
      update: { activeTable: tableName },
      create: {
        formId: form.id,
        activeTable: tableName,
        viewName: `form_${form.key}_active`,
      },
    });

    return {
      tableName,
      ddl,
      status: 'created',
    };
  }

  private buildCreateTableDDL(tableName: string, fields: FormField[]): string {
    const columns = [
      'id uuid PRIMARY KEY DEFAULT gen_random_uuid()',
      'created_at timestamptz NOT NULL DEFAULT now()',
      'updated_at timestamptz NOT NULL DEFAULT now()',
      '_deleted boolean NOT NULL DEFAULT false',
    ];

    // Add user fields
    fields.forEach(field => {
      const columnDef = this.getColumnDefinition(field);
      columns.push(columnDef);
    });

    // Add indexes for unique fields
    const uniqueIndexes = fields
      .filter(field => field.unique)
      .map(field => `CREATE UNIQUE INDEX ON ${tableName} (${field.key})`);

    // Add indexes for frequently filtered fields
    const filterIndexes = fields
      .filter(field => field.type === 'DATE' || field.type === 'DATETIME' || field.type === 'BOOLEAN')
      .map(field => `CREATE INDEX ON ${tableName} (${field.key})`);

    const ddl = `
CREATE TABLE ${tableName} (
  ${columns.join(',\n  ')}
);

${uniqueIndexes.join('\n')}
${filterIndexes.join('\n')}

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_${tableName}_updated_at
BEFORE UPDATE ON ${tableName}
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Active view (optional)
CREATE OR REPLACE VIEW form_${tableName.split('_')[1]}_active AS
SELECT * FROM ${tableName} WHERE _deleted = false;
    `.trim();

    return ddl;
  }

  private getColumnDefinition(field: FormField): string {
    const columnName = field.key;
    let columnType = this.getPostgreSQLType(field.type);
    
    // Add constraints
    const constraints = [];
    
    if (field.required) {
      constraints.push('NOT NULL');
    }
    
    if (field.defaultValue !== null && field.defaultValue !== undefined) {
      constraints.push(`DEFAULT '${field.defaultValue}'`);
    }

    // Add length constraints for text fields
    if (field.type === 'SHORT_TEXT' && field.maxLength) {
      columnType = `varchar(${field.maxLength})`;
    } else if (field.type === 'LONG_TEXT') {
      columnType = 'text';
    }

    // Add precision for decimal fields
    if (field.type === 'DECIMAL') {
      columnType = 'decimal(10,2)';
    }

    // Add enum constraints
    if (field.type === 'ENUM' && field.enumOptions && field.enumOptions.length > 0) {
      const enumValues = field.enumOptions.map(opt => `'${opt}'`).join(', ');
      constraints.push(`CHECK (${columnName} IN (${enumValues}))`);
    }

    return `${columnName} ${columnType} ${constraints.join(' ')}`;
  }

  private getPostgreSQLType(fieldType: FieldType): string {
    const typeMap = {
      SHORT_TEXT: 'varchar(255)',
      LONG_TEXT: 'text',
      NUMBER: 'integer',
      DECIMAL: 'decimal(10,2)',
      BOOLEAN: 'boolean',
      DATE: 'date',
      DATETIME: 'timestamptz',
      EMAIL: 'varchar(320)',
      PHONE: 'varchar(20)',
      ENUM: 'text',
      JSON: 'jsonb',
      FILE_REF: 'jsonb',
      RELATION: 'uuid',
    };

    return typeMap[fieldType] || 'text';
  }

  async executeDDL(ddl: string): Promise<void> {
    // This would execute the DDL against the database
    // In a real implementation, you'd use a database connection
    // For now, we'll just log it
    console.log('Executing DDL:', ddl);
    
    // TODO: Implement actual DDL execution
    // This could be done using raw SQL queries through Prisma
    // or by using a dedicated database migration tool
  }

  async getTableInfo(tableName: string) {
    // This would return information about the table structure
    // In a real implementation, you'd query the database metadata
    return {
      tableName,
      columns: [],
      indexes: [],
      constraints: [],
    };
  }
}


