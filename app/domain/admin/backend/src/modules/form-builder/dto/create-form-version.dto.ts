import { IsString, IsOptional, IsArray, ValidateNested, IsEnum, IsBoolean, IsNumber, IsObject } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty } from '@nestjs/swagger';
import { FieldType } from '@prisma/client';

export class FormFieldDto {
  @ApiProperty({ example: 'First Name' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'first_name' })
  @IsString()
  key: string;

  @ApiProperty({ example: 'SHORT_TEXT', enum: FieldType })
  @IsEnum(FieldType)
  type: FieldType;

  @ApiProperty({ example: false, required: false })
  @IsOptional()
  @IsBoolean()
  required?: boolean;

  @ApiProperty({ example: false, required: false })
  @IsOptional()
  @IsBoolean()
  unique?: boolean;

  @ApiProperty({ example: 'John', required: false })
  @IsOptional()
  @IsString()
  defaultValue?: string;

  @ApiProperty({ example: 1, required: false })
  @IsOptional()
  @IsNumber()
  minLength?: number;

  @ApiProperty({ example: 120, required: false })
  @IsOptional()
  @IsNumber()
  maxLength?: number;

  @ApiProperty({ example: 0, required: false })
  @IsOptional()
  @IsNumber()
  minValue?: number;

  @ApiProperty({ example: 100, required: false })
  @IsOptional()
  @IsNumber()
  maxValue?: number;

  @ApiProperty({ example: '^[a-zA-Z]+$', required: false })
  @IsOptional()
  @IsString()
  regex?: string;

  @ApiProperty({ example: ['option1', 'option2'], required: false })
  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  enumOptions?: string[];

  @ApiProperty({ required: false })
  @IsOptional()
  @IsObject()
  relation?: any;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsObject()
  ui?: any;
}

export class CreateFormVersionDto {
  @ApiProperty({ example: 'v1' })
  @IsString()
  displayName: string;

  @ApiProperty({ example: 'Initial version', required: false })
  @IsOptional()
  @IsString()
  description?: string;

  @ApiProperty({ example: 'default', required: false })
  @IsOptional()
  @IsString()
  validationPreset?: string;

  @ApiProperty({ type: [FormFieldDto], required: false })
  @IsOptional()
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => FormFieldDto)
  fields?: FormFieldDto[];
}


