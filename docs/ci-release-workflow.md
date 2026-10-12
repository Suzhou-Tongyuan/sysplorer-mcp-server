# Sysplorer MCP Server CI/CD 打包与发布规则

本文说明本仓库流水线在不同分支、Tag 和变量下的触发规则、构建产物及发布方式。实际行为以仓库根目录的 [`.gitlab-ci.yml`](../.gitlab-ci.yml) 为准。

## 触发规则

| 触发方式 | Windows 构建 | Linux 构建 | 汇总 Artifact | 上传 OSS | 创建 GitLab Release | 同步 GitHub |
| --- | --- | --- | --- | --- | --- | --- |
| 普通分支 Push | 是 | 是 | 是 | 否 | 否 | 否 |
| Merge Request 流水线 | 是 | 是 | 是 | 否 | 否 | 否 |
| `develop` 手动运行并设置 `VERSION` | 是 | 是 | 是 | 是 | 是 | 否 |
| `v*` Tag，例如 `v20260819_1` | 是 | 是 | 是 | 是 | 是 | 否 |
| 其他非 `publish-*` Tag | 是 | 是 | 是 | 否 | 否 | 否 |
| `publish-*` Tag | 否 | 否 | 否 | 否 | 否 | 是 |

说明：

- 普通分支和 Merge Request 用于持续验证构建，不会写入 OSS，也不会创建 Release。
- 正式发布只接受 `v*` Tag，或在 `develop` 分支手动运行流水线并设置 `VERSION`。
- `publish-*` Tag 是独立的 GitHub 同步入口，不参与本仓库的打包和 OSS 发布。
- 项目已将 `v*` 配置为受保护 Tag，只有 Maintainer 可以创建正式发布 Tag。

## 流水线阶段

流水线按以下顺序执行：

1. `build_windows`：在 Windows x86_64 Runner 中调用 `install/build_publish.ps1` 构建 Windows 包。
2. `build_linux`：在 Linux x86_64 Runner 中调用 `install/linux/scripts/build_publish.sh` 构建 Linux 包。
3. `package_release_assets`：汇总两个平台的包，生成 `SHA256SUMS`，并立即校验文件摘要。
4. `upload_release_assets`：仅在正式发布条件下上传到内部 OSS。
5. `release`：仅在 OSS 上传成功后创建 GitLab Release，并添加 OSS 下载链接。
6. `sync_to_github`：仅由 `publish-*` Tag 触发，与上述构建发布链路互斥。

前一阶段失败时，依赖它的后续阶段不会继续。例如任一平台构建失败，都不会上传不完整的发布目录。

## 构建模式

流水线根据触发方式自动选择构建模式：

- 普通分支和 Merge Request：内部构建模式，Windows 脚本使用 `-Internal`，Linux 脚本使用 `--internal`。
- 任意非 `publish-*` Tag：发布构建模式，不附加内部构建参数。
- `develop + VERSION`：发布构建模式，不附加内部构建参数。

应用包的基础版本由 `install/package_version.json` 和构建脚本生成。`VERSION` 或 Git Tag 同时用作 OSS 发布目录名和 GitLab Release Tag，不会直接改写源码中的版本文件。

## 构建产物

`package_release_assets` 会生成以下稳定文件名：

```text
dist/
├── SHA256SUMS
├── sysplorer-mcp-server-glnxa64.zip
└── sysplorer-mcp-server-win64.zip
```

这些文件会作为 GitLab Job Artifact 保存 30 天。普通分支和 Merge Request 可直接从 `package_release_assets` Job 下载，无需发布到 OSS。

两个 ZIP 内都必须包含：

```text
sysplorer_mcp/MCP_BUILD_INFO.json
```

流水线会在两个平台的构建阶段检查该文件，并在汇总阶段通过 `SHA256SUMS` 校验两个 ZIP 的完整性。

## 正式发布方法

### 方法一：推送 `v*` Tag

在准备发布的提交上创建受保护 Tag：

```bash
git switch develop
git pull --ff-only
git tag v20260819_1
git push origin v20260819_1
```

该 Tag 会依次触发 Windows 构建、Linux 构建、产物汇总、OSS 上传和 GitLab Release 创建。

### 方法二：在 `develop` 上设置 `VERSION`

在 GitLab 项目中进入 **Build > Pipelines > New pipeline**：

1. 分支选择 `develop`。
2. 增加变量 `VERSION`，例如 `v20260819_1`。
3. 运行流水线。

该方式会以当前 `develop` 的提交 SHA 创建发布。`VERSION` 必须使用新的、未被其他内容占用的发布标识。

## OSS 目录

正式发布产物保存到：

```text
https://oss-dev.tongyuan.cc/ai-assets/sysplorer-mcp-server/<RELEASE_TAG>/
```

例如：

```text
https://oss-dev.tongyuan.cc/ai-assets/sysplorer-mcp-server/v20260819_1/
├── SHA256SUMS
├── sysplorer-mcp-server-glnxa64.zip
└── sysplorer-mcp-server-win64.zip
```

其中 `<RELEASE_TAG>` 的取值优先级为：

1. 手动流水线变量 `VERSION`。
2. Git Tag `CI_COMMIT_TAG`。

上传脚本采用不可变发布策略：目标文件不存在时上传；同名且内容一致时视为成功；同名但内容不一致时拒绝覆盖。需要重新发布时应使用新的版本标识，不要覆盖已有目录。

## CI 配置要求

项目 CI/CD Variables 必须配置以下变量：

| 变量 | 用途 | 要求 |
| --- | --- | --- |
| `MINIO_ASSETS_AK` | OSS Access Key | Masked、Protected |
| `MINIO_ASSETS_SK` | OSS Secret Key | Masked、Protected |

凭据不得写入仓库。由于变量是 Protected，正式发布应使用受保护的 `v*` Tag；如调整分支保护规则，需要同时确认发布 Job 能否读取这两个变量。

## 发布验证

发布完成后按以下顺序检查：

1. 确认 `build_windows`、`build_linux`、`package_release_assets`、`upload_release_assets` 和 `release` 全部成功。
2. 从 OSS 下载三个文件，并校验摘要：

   ```bash
   sha256sum --check SHA256SUMS
   ```

3. 检查 OSS 对象可访问：

   ```bash
   curl -I "https://oss-dev.tongyuan.cc/ai-assets/sysplorer-mcp-server/v20260819_1/sysplorer-mcp-server-glnxa64.zip"
   curl -I "https://oss-dev.tongyuan.cc/ai-assets/sysplorer-mcp-server/v20260819_1/sysplorer-mcp-server-win64.zip"
   ```

4. 打开对应 GitLab Release，确认 Windows、Linux 和 `SHA256SUMS` 三个链接均指向同一个版本目录。

## 常见情况

- 普通 `develop` Push 没有上传 OSS：符合预期；未设置 `VERSION` 时只执行构建验证。
- `publish-*` Tag 没有产生安装包：符合预期；该 Tag 只用于同步 GitHub。
- OSS 提示目标文件内容不同：发布目录已存在且内容不一致；使用新的发布标识重新运行，不要覆盖旧版本。
- Release Job 未执行：检查 Tag 是否以 `v` 开头，或手动流水线是否同时满足分支为 `develop` 且设置了 `VERSION`。
- 发布 Job 无法读取 OSS 凭据：检查触发引用是否受保护，以及 `MINIO_ASSETS_AK`、`MINIO_ASSETS_SK` 是否仍为 Protected 变量。
