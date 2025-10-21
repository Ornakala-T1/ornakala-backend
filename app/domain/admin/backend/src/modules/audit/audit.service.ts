import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../common/prisma/prisma.service';

@Injectable()
export class AuditService {
  constructor(private prisma: PrismaService) {}

  async logAction(
    actorUserId: string,
    action: string,
    resourceType: string,
    resourceId?: string,
    metadata?: any,
    ip?: string,
    userAgent?: string,
  ) {
    return this.prisma.auditLog.create({
      data: {
        actorUserId,
        action,
        resourceType,
        resourceId,
        metadata,
        ip,
        userAgent,
      },
    });
  }

  async getAuditLogs(
    page = 1,
    pageSize = 50,
    actorUserId?: string,
    action?: string,
    resourceType?: string,
    resourceId?: string,
  ) {
    const where: any = {};

    if (actorUserId) {
      where.actorUserId = actorUserId;
    }

    if (action) {
      where.action = action;
    }

    if (resourceType) {
      where.resourceType = resourceType;
    }

    if (resourceId) {
      where.resourceId = resourceId;
    }

    const [logs, total] = await Promise.all([
      this.prisma.auditLog.findMany({
        where,
        include: {
          actor: {
            select: {
              id: true,
              name: true,
              email: true,
            },
          },
        },
        orderBy: {
          timestamp: 'desc',
        },
        skip: (page - 1) * pageSize,
        take: pageSize,
      }),
      this.prisma.auditLog.count({ where }),
    ]);

    return {
      logs,
      pagination: {
        page,
        pageSize,
        total,
        totalPages: Math.ceil(total / pageSize),
      },
    };
  }

  async getAuditLogById(id: string) {
    return this.prisma.auditLog.findUnique({
      where: { id },
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

  async getAuditLogsForResource(resourceType: string, resourceId: string) {
    return this.prisma.auditLog.findMany({
      where: {
        resourceType,
        resourceId,
      },
      include: {
        actor: {
          select: {
            id: true,
            name: true,
            email: true,
          },
        },
      },
      orderBy: {
        timestamp: 'desc',
      },
    });
  }
}


