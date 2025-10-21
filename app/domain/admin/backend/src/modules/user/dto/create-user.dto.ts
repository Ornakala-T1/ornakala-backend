import { IsEmail, IsString, IsOptional, IsEnum } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { UserStatus } from '@prisma/client';

export class CreateUserDto {
  @ApiProperty({ example: 'developer@ornakala.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'John Developer' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'INVITED', enum: UserStatus, required: false })
  @IsOptional()
  @IsEnum(UserStatus)
  status?: UserStatus;
}


