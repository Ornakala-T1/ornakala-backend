import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ThrottlerModule } from '@nestjs/throttler';
import { PrismaModule } from './common/prisma/prisma.module';
import { AuthModule } from './modules/auth/auth.module';
import { UserModule } from './modules/user/user.module';
import { RbacModule } from './modules/rbac/rbac.module';
import { FormBuilderModule } from './modules/form-builder/form-builder.module';
import { SchemaModule } from './modules/schema/schema.module';
import { DataModule } from './modules/data/data.module';
import { AuditModule } from './modules/audit/audit.module';
import { AdminExploreModule } from './modules/admin-explore/admin-explore.module';
import { HealthController } from './health.controller';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
    ThrottlerModule.forRoot([
      {
        ttl: 60000, // 1 minute
        limit: 100, // 100 requests per minute
      },
    ]),
    PrismaModule,
    AuthModule,
    UserModule,
    RbacModule,
    FormBuilderModule,
    SchemaModule,
    DataModule,
    AuditModule,
    AdminExploreModule,
  ],
  controllers: [HealthController],
})
export class AppModule {}
