import { IsString, IsEnum, IsOptional } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { ResourceType, Action } from '@prisma/client';

export class CreatePermissionDto {
  @ApiProperty({ example: 'FORM', enum: ResourceType })
  @IsEnum(ResourceType)
  resourceType: ResourceType;

  @ApiProperty({ example: 'EDIT', enum: Action })
  @IsEnum(Action)
  action: Action;

  @ApiProperty({ example: 'form-uuid', required: false })
  @IsOptional()
  @IsString()
  resourceId?: string;
}


