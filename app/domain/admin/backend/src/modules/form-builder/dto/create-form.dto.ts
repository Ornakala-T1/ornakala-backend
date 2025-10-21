import { IsString, IsOptional, Matches } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateFormDto {
  @ApiProperty({ example: 'Customer Management' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'customer' })
  @IsString()
  @Matches(/^[a-z0-9_]+$/, { message: 'Key must contain only lowercase letters, numbers, and underscores' })
  key: string;

  @ApiProperty({ example: 'Customer master data management', required: false })
  @IsOptional()
  @IsString()
  description?: string;
}


