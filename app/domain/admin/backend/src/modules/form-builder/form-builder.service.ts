import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../../common/prisma/prisma.service';
import { CreateFormDto } from './dto/create-form.dto';
import { UpdateFormDto } from './dto/update-form.dto';
import { CreateFormVersionDto } from './dto/create-form-version.dto';
import { Form, FormStatus } from '@prisma/client';

@Injectable()
export class FormBuilderService {
  constructor(private prisma: PrismaService) {}

  async createForm(createFormDto: CreateFormDto, userId: string) {
    // Check if form key already exists
    const existingForm = await this.prisma.form.findUnique({
      where: { key: createFormDto.key },
    });

    if (existingForm) {
      throw new BadRequestException('Form with this key already exists');
    }

    return this.prisma.form.create({
      data: {
        ...createFormDto,
        createdBy: userId,
      },
      include: {
        creator: true,
        versions: {
          include: {
            fields: true,
          },
        },
      },
    });
  }

  async findAllForms() {
    return this.prisma.form.findMany({
      include: {
        creator: true,
        versions: {
          include: {
            fields: true,
          },
        },
        tableAlias: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
  }

  async findFormById(id: string) {
    const form = await this.prisma.form.findUnique({
      where: { id },
      include: {
        creator: true,
        versions: {
          include: {
            fields: true,
          },
          orderBy: {
            version: 'desc',
          },
        },
        tableAlias: true,
        tableSettings: true,
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    return form;
  }

  async findFormByKey(key: string) {
    const form = await this.prisma.form.findUnique({
      where: { key },
      include: {
        creator: true,
        versions: {
          include: {
            fields: true,
          },
          orderBy: {
            version: 'desc',
          },
        },
        tableAlias: true,
        tableSettings: true,
      },
    });

    if (!form) {
      throw new NotFoundException('Form not found');
    }

    return form;
  }

  async updateForm(id: string, updateFormDto: UpdateFormDto) {
    const form = await this.findFormById(id);

    return this.prisma.form.update({
      where: { id },
      data: updateFormDto,
      include: {
        creator: true,
        versions: {
          include: {
            fields: true,
          },
        },
        tableAlias: true,
      },
    });
  }

  async deleteForm(id: string) {
    const form = await this.findFormById(id);

    return this.prisma.form.update({
      where: { id },
      data: { status: 'ARCHIVED' },
    });
  }

  async createFormVersion(formId: string, createFormVersionDto: CreateFormVersionDto) {
    const form = await this.findFormById(formId);

    // Get the next version number
    const nextVersion = form.currentVersion + 1;

    // Create the new version
    const version = await this.prisma.formVersion.create({
      data: {
        formId,
        version: nextVersion,
        displayName: createFormVersionDto.displayName,
        description: createFormVersionDto.description,
        validationPreset: createFormVersionDto.validationPreset,
      },
    });

    // Create the fields
    if (createFormVersionDto.fields && createFormVersionDto.fields.length > 0) {
      await this.prisma.formField.createMany({
        data: createFormVersionDto.fields.map(field => ({
          formVersionId: version.id,
          ...field,
        })),
      });
    }

    return this.prisma.formVersion.findUnique({
      where: { id: version.id },
      include: {
        fields: true,
        form: true,
      },
    });
  }

  async publishForm(formId: string) {
    const form = await this.findFormById(formId);
    
    if (form.status === 'ACTIVE') {
      throw new BadRequestException('Form is already published');
    }

    // Get the latest version
    const latestVersion = await this.prisma.formVersion.findFirst({
      where: { formId },
      orderBy: { version: 'desc' },
      include: { fields: true },
    });

    if (!latestVersion) {
      throw new BadRequestException('No version found for this form');
    }

    // Update form status and version
    await this.prisma.form.update({
      where: { id: formId },
      data: {
        status: 'ACTIVE',
        currentVersion: latestVersion.version,
      },
    });

    // TODO: Trigger schema generation and table creation
    // This will be handled by the SchemaModule

    return {
      formId,
      version: latestVersion.version,
      status: 'ACTIVE',
      message: 'Form published successfully. Schema generation will be triggered.',
    };
  }

  async getFormVersion(formId: string, version: number) {
    const formVersion = await this.prisma.formVersion.findFirst({
      where: {
        formId,
        version,
      },
      include: {
        fields: true,
        form: true,
      },
    });

    if (!formVersion) {
      throw new NotFoundException('Form version not found');
    }

    return formVersion;
  }
}


