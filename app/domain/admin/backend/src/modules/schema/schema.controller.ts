import { Controller, Get, Post, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { SchemaService } from './schema.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@ApiTags('Schema')
@Controller('schema')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class SchemaController {
  constructor(private readonly schemaService: SchemaService) {}

  @Post('generate/:formId')
  @ApiOperation({ summary: 'Generate table schema for a form' })
  @ApiResponse({ status: 200, description: 'Schema generated successfully' })
  async generateSchema(@Param('formId') formId: string) {
    // This would be called when a form is published
    // The actual implementation would fetch the form and its fields
    // and generate the appropriate DDL
    return { message: 'Schema generation triggered' };
  }

  @Get('tables/:tableName')
  @ApiOperation({ summary: 'Get table information' })
  @ApiResponse({ status: 200, description: 'Table information retrieved' })
  async getTableInfo(@Param('tableName') tableName: string) {
    return this.schemaService.getTableInfo(tableName);
  }
}


