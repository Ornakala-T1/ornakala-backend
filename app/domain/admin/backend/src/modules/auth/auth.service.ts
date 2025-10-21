import { Injectable, UnauthorizedException, BadRequestException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { PrismaService } from '../../common/prisma/prisma.service';
import * as argon2 from 'argon2';
import { LoginDto } from './dto/login.dto';
import { RegisterDto } from './dto/register.dto';
import { User } from '@prisma/client';

@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
  ) {}

  async validateUser(email: string, password: string): Promise<User | null> {
    const user = await this.prisma.user.findUnique({
      where: { email },
    });

    if (!user || user.status !== 'ACTIVE') {
      return null;
    }

    const isPasswordValid = await argon2.verify(user.passwordHash, password);
    if (!isPasswordValid) {
      return null;
    }

    return user;
  }

  async login(loginDto: LoginDto) {
    const user = await this.validateUser(loginDto.email, loginDto.password);
    
    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    // TODO: Implement MFA verification if enabled
    if (user.mfaSecret && !loginDto.mfaCode) {
      throw new BadRequestException('MFA code required');
    }

    const payload = { 
      sub: user.id, 
      email: user.email, 
      name: user.name 
    };

    return {
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        status: user.status,
      },
    };
  }

  async register(registerDto: RegisterDto) {
    const existingUser = await this.prisma.user.findUnique({
      where: { email: registerDto.email },
    });

    if (existingUser) {
      throw new BadRequestException('User already exists');
    }

    const passwordHash = await argon2.hash(registerDto.password);
    
    const user = await this.prisma.user.create({
      data: {
        email: registerDto.email,
        name: registerDto.name,
        passwordHash,
        status: 'ACTIVE',
      },
    });

    // Assign default role (you might want to create a default role)
    // await this.assignDefaultRole(user.id);

    const payload = { 
      sub: user.id, 
      email: user.email, 
      name: user.name 
    };

    return {
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        status: user.status,
      },
    };
  }

  async logout() {
    // In a stateless JWT system, logout is handled client-side
    // You might want to implement a blacklist for JWT tokens
    return { message: 'Logged out successfully' };
  }

  async refreshToken(user: User) {
    const payload = { 
      sub: user.id, 
      email: user.email, 
      name: user.name 
    };

    return {
      access_token: this.jwtService.sign(payload),
    };
  }
}


