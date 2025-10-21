import { IsString, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateRoleDto {
  @ApiProperty({ example: 'form-editor' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'Can edit forms and data', required: false })
  @IsOptional()
  @IsString()
  description?: string;
}


