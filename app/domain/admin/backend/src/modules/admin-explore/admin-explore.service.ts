import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../common/prisma/prisma.service';

@Injectable()
export class AdminExploreService {
  constructor(private prisma: PrismaService) {}

  async getDashboardStats() {
    const [
      totalUsers,
      totalForms,
      activeForms,
      totalRecords,
    ] = await Promise.all([
      this.prisma.user.count(),
      this.prisma.form.count(),
      this.prisma.form.count({ where: { status: 'ACTIVE' } }),
      // TODO: Implement total records count from all dynamic tables
      0,
    ]);

    return {
      totalUsers,
      totalForms,
      activeForms,
      totalRecords,
    };
  }

  async getAllTables() {
    const forms = await this.prisma.form.findMany({
      include: {
        tableAlias: true,
        tableSettings: true,
        creator: true,
        versions: {
          orderBy: { version: 'desc' },
          take: 1,
          include: { fields: true },
        },
      },
      orderBy: { createdAt: 'desc' },
    });

    return forms.map(form => ({
      id: form.id,
      name: form.name,
      key: form.key,
      status: form.status,
      tableName: form.tableAlias?.activeTable,
      viewName: form.tableAlias?.viewName,
      creator: form.creator,
      createdAt: form.createdAt,
      updatedAt: form.updatedAt,
      fieldCount: form.versions[0]?.fields.length || 0,
      settings: form.tableSettings,
    }));
  }

  async getTableDetails(formId: string) {
    const form = await this.prisma.form.findUnique({
      where: { id: formId },
      include: {
        tableAlias: true,
        tableSettings: true,
        creator: true,
        versions: {
          orderBy: { version: 'desc' },
          take: 1,
          include: { fields: true },
        },
      },
    });

    if (!form) {
      return null;
    }

    return {
      id: form.id,
      name: form.name,
      key: form.key,
      status: form.status,
      tableName: form.tableAlias?.activeTable,
      viewName: form.tableAlias?.viewName,
      creator: form.creator,
      createdAt: form.createdAt,
      updatedAt: form.updatedAt,
      fields: form.versions[0]?.fields || [],
      settings: form.tableSettings,
    };
  }

  async updateTableSettings(formId: string, settings: any) {
    return this.prisma.tableSetting.upsert({
      where: { formId },
      update: settings,
      create: {
        formId,
        ...settings,
      },
    });
  }

  async getRecentActivity(limit = 10) {
    return this.prisma.auditLog.findMany({
      take: limit,
      orderBy: { timestamp: 'desc' },
      include: {
        actor: {
          select: {
            id: true,
            name: true,
            email: true,
          },
        },
      },
    });
  }
}
