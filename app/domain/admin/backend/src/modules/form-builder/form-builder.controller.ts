import { Controller, Get, Post, Body, Patch, Param, Delete, UseGuards, Request } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { FormBuilderService } from './form-builder.service';
import { CreateFormDto } from './dto/create-form.dto';
import { UpdateFormDto } from './dto/update-form.dto';
import { CreateFormVersionDto } from './dto/create-form-version.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@ApiTags('Form Builder')
@Controller('forms')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class FormBuilderController {
  constructor(private readonly formBuilderService: FormBuilderService) {}

  @Post()
  @ApiOperation({ summary: 'Create a new form' })
  @ApiResponse({ status: 201, description: 'Form created successfully' })
  @ApiResponse({ status: 400, description: 'Form key already exists' })
  createForm(@Body() createFormDto: CreateFormDto, @Request() req) {
    return this.formBuilderService.createForm(createFormDto, req.user.id);
  }

  @Get()
  @ApiOperation({ summary: 'Get all forms' })
  @ApiResponse({ status: 200, description: 'Forms retrieved successfully' })
  findAllForms() {
    return this.formBuilderService.findAllForms();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get form by ID' })
  @ApiResponse({ status: 200, description: 'Form retrieved successfully' })
  @ApiResponse({ status: 404, description: 'Form not found' })
  findFormById(@Param('id') id: string) {
    return this.formBuilderService.findFormById(id);
  }

  @Get('key/:key')
  @ApiOperation({ summary: 'Get form by key' })
  @ApiResponse({ status: 200, description: 'Form retrieved successfully' })
  @ApiResponse({ status: 404, description: 'Form not found' })
  findFormByKey(@Param('key') key: string) {
    return this.formBuilderService.findFormByKey(key);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update form' })
  @ApiResponse({ status: 200, description: 'Form updated successfully' })
  @ApiResponse({ status: 404, description: 'Form not found' })
  updateForm(@Param('id') id: string, @Body() updateFormDto: UpdateFormDto) {
    return this.formBuilderService.updateForm(id, updateFormDto);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete form (archive)' })
  @ApiResponse({ status: 200, description: 'Form deleted successfully' })
  @ApiResponse({ status: 404, description: 'Form not found' })
  deleteForm(@Param('id') id: string) {
    return this.formBuilderService.deleteForm(id);
  }

  @Post(':id/versions')
  @ApiOperation({ summary: 'Create a new form version' })
  @ApiResponse({ status: 201, description: 'Form version created successfully' })
  @ApiResponse({ status: 404, description: 'Form not found' })
  createFormVersion(@Param('id') id: string, @Body() createFormVersionDto: CreateFormVersionDto) {
    return this.formBuilderService.createFormVersion(id, createFormVersionDto);
  }

  @Post(':id/publish')
  @ApiOperation({ summary: 'Publish form (make it active)' })
  @ApiResponse({ status: 200, description: 'Form published successfully' })
  @ApiResponse({ status: 400, description: 'Form already published or no version found' })
  publishForm(@Param('id') id: string) {
    return this.formBuilderService.publishForm(id);
  }

  @Get(':id/versions/:version')
  @ApiOperation({ summary: 'Get specific form version' })
  @ApiResponse({ status: 200, description: 'Form version retrieved successfully' })
  @ApiResponse({ status: 404, description: 'Form version not found' })
  getFormVersion(@Param('id') id: string, @Param('version') version: string) {
    return this.formBuilderService.getFormVersion(id, parseInt(version));
  }
}


