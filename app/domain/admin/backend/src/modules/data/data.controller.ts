import { Controller, Get, Post, Body, Patch, Param, Delete, UseGuards, Request, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { DataService } from './data.service';
import { CreateRecordDto } from './dto/create-record.dto';
import { UpdateRecordDto } from './dto/update-record.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@ApiTags('Data')
@Controller('data')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class DataController {
  constructor(private readonly dataService: DataService) {}

  @Get(':formKey')
  @ApiOperation({ summary: 'Get all records for a form' })
  @ApiResponse({ status: 200, description: 'Records retrieved successfully' })
  async findAll(
    @Param('formKey') formKey: string,
    @Query('page') page?: number,
    @Query('pageSize') pageSize?: number,
    @Query('includeDeleted') includeDeleted?: boolean,
  ) {
    return this.dataService.findAll(formKey, page, pageSize, includeDeleted);
  }

  @Get(':formKey/:id')
  @ApiOperation({ summary: 'Get a specific record' })
  @ApiResponse({ status: 200, description: 'Record retrieved successfully' })
  @ApiResponse({ status: 404, description: 'Record not found' })
  async findOne(@Param('formKey') formKey: string, @Param('id') id: string) {
    return this.dataService.findOne(formKey, id);
  }

  @Post(':formKey')
  @ApiOperation({ summary: 'Create a new record' })
  @ApiResponse({ status: 201, description: 'Record created successfully' })
  @ApiResponse({ status: 400, description: 'Validation error' })
  async create(
    @Param('formKey') formKey: string,
    @Body() createRecordDto: CreateRecordDto,
    @Request() req,
  ) {
    return this.dataService.create(formKey, createRecordDto, req.user.id);
  }

  @Patch(':formKey/:id')
  @ApiOperation({ summary: 'Update a record' })
  @ApiResponse({ status: 200, description: 'Record updated successfully' })
  @ApiResponse({ status: 404, description: 'Record not found' })
  async update(
    @Param('formKey') formKey: string,
    @Param('id') id: string,
    @Body() updateRecordDto: UpdateRecordDto,
    @Request() req,
  ) {
    return this.dataService.update(formKey, id, updateRecordDto, req.user.id);
  }

  @Delete(':formKey/:id')
  @ApiOperation({ summary: 'Delete a record (soft delete)' })
  @ApiResponse({ status: 200, description: 'Record deleted successfully' })
  @ApiResponse({ status: 404, description: 'Record not found' })
  async remove(
    @Param('formKey') formKey: string,
    @Param('id') id: string,
    @Request() req,
  ) {
    return this.dataService.remove(formKey, id, req.user.id);
  }

  @Post(':formKey/:id/restore')
  @ApiOperation({ summary: 'Restore a deleted record' })
  @ApiResponse({ status: 200, description: 'Record restored successfully' })
  @ApiResponse({ status: 404, description: 'Record not found' })
  async restore(
    @Param('formKey') formKey: string,
    @Param('id') id: string,
    @Request() req,
  ) {
    return this.dataService.restore(formKey, id, req.user.id);
  }
}


