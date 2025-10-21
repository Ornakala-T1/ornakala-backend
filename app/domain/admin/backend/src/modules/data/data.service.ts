import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../../common/prisma/prisma.service';
import { CreateRecordDto } from './dto/create-record.dto';
import { UpdateRecordDto } from './dto/update-record.dto';

@Injectable()
export class DataService {
  constructor(private prisma: PrismaService) {}

  async findAll(formKey: string, page = 1, pageSize = 10, includeDeleted = false) {
    // Get the form and its active table
    const form = await this.prisma.form.findUnique({
      where: { key: formKey },
      include: {
        tableAlias: true,
        versions: {
          where: { version: { gte: 1 } },
          orderBy: { version: 'desc' },
          take: 1,
          include: { fields: true },
        },
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    if (!form.tableAlias) {
      throw new BadRequestException('Form table not created yet');
    }

    // TODO: Implement actual data fetching from the dynamic table
    // This would require raw SQL queries or a more sophisticated approach
    // For now, return a placeholder response
    return {
      data: [],
      pagination: {
        page,
        pageSize,
        total: 0,
        totalPages: 0,
      },
    };
  }

  async findOne(formKey: string, id: string) {
    // Get the form and its active table
    const form = await this.prisma.form.findUnique({
      where: { key: formKey },
      include: {
        tableAlias: true,
        versions: {
          where: { version: { gte: 1 } },
          orderBy: { version: 'desc' },
          take: 1,
          include: { fields: true },
        },
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    if (!form.tableAlias) {
      throw new BadRequestException('Form table not created yet');
    }

    // TODO: Implement actual data fetching from the dynamic table
    return { id, formKey, data: {} };
  }

  async create(formKey: string, createRecordDto: CreateRecordDto, userId: string) {
    // Get the form and its active table
    const form = await this.prisma.form.findUnique({
      where: { key: formKey },
      include: {
        tableAlias: true,
        versions: {
          where: { version: { gte: 1 } },
          orderBy: { version: 'desc' },
          take: 1,
          include: { fields: true },
        },
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    if (!form.tableAlias) {
      throw new BadRequestException('Form table not created yet');
    }

    // Validate data against form schema
    this.validateDataAgainstSchema(createRecordDto, form.versions[0].fields);

    // TODO: Implement actual data insertion into the dynamic table
    // This would require raw SQL queries or a more sophisticated approach
    return { id: 'generated-id', formKey, data: createRecordDto };
  }

  async update(formKey: string, id: string, updateRecordDto: UpdateRecordDto, userId: string) {
    // Get the form and its active table
    const form = await this.prisma.form.findUnique({
      where: { key: formKey },
      include: {
        tableAlias: true,
        versions: {
          where: { version: { gte: 1 } },
          orderBy: { version: 'desc' },
          take: 1,
          include: { fields: true },
        },
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    if (!form.tableAlias) {
      throw new BadRequestException('Form table not created yet');
    }

    // Validate data against form schema
    this.validateDataAgainstSchema(updateRecordDto, form.versions[0].fields);

    // TODO: Implement actual data update in the dynamic table
    return { id, formKey, data: updateRecordDto };
  }

  async remove(formKey: string, id: string, userId: string) {
    // Get the form and its active table
    const form = await this.prisma.form.findUnique({
      where: { key: formKey },
      include: {
        tableAlias: true,
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    if (!form.tableAlias) {
      throw new BadRequestException('Form table not created yet');
    }

    // TODO: Implement soft delete in the dynamic table
    return { id, formKey, deleted: true };
  }

  async restore(formKey: string, id: string, userId: string) {
    // Get the form and its active table
    const form = await this.prisma.form.findUnique({
      where: { key: formKey },
      include: {
        tableAlias: true,
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    if (!form.tableAlias) {
      throw new BadRequestException('Form table not created yet');
    }

    // TODO: Implement restore in the dynamic table
    return { id, formKey, restored: true };
  }

  private validateDataAgainstSchema(data: any, fields: any[]) {
    // This would implement validation against the form schema
    // For now, just a placeholder
    console.log('Validating data against schema:', data, fields);
  }
}


