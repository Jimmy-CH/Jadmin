/**
 * API响应码枚举
 */
export const enum ApiCodeEnum {
  /**
   * 成功
   */
  SUCCESS = "200",
  /**
   * 错误
   */
  ERROR = "500",

  /**
   * 访问令牌无效或过期
   */
  ACCESS_TOKEN_INVALID = "401",

  /**
   * 刷新令牌无效或过期
   */
  REFRESH_TOKEN_INVALID = "A0231",
}
